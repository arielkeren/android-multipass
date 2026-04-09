import Java from "frida-java-bridge";

let config;

const WRONG_PASSWORD = "0";
const RESPONSE_OK = 0;

const LOCK_SETTINGS_SERVICE_CLASS_NAME =
  "com.android.server.locksettings.LockSettingsService";
const ACTIVITY_THREAD_CLASS_NAME = "android.app.ActivityThread";
const KEYGUARD_MANAGER_CLASS_NAME = "android.app.KeyguardManager";

const KEYGUARD_SERVICE_NAME = "keyguard";

const stringToBytes = string =>
  string.split("").map(char => char.charCodeAt(0));

const bytesToString = bytes => {
  let out = "";
  for (let i = 0; i < bytes.length; i++) {
    out += String.fromCharCode(bytes[i]);
  }
  return out;
};

const getDoVerifyCredential = () => {
  const LockSettingsService = Java.use(LOCK_SETTINGS_SERVICE_CLASS_NAME);
  return LockSettingsService.doVerifyCredential;
};

const getKeyguardManager = () => {
  const ActivityThread = Java.use(ACTIVITY_THREAD_CLASS_NAME);
  const app = ActivityThread.currentApplication();
  const ctx = app.getApplicationContext();

  const KeyguardManager = Java.use(KEYGUARD_MANAGER_CLASS_NAME);
  return Java.cast(
    ctx.getSystemService(KEYGUARD_SERVICE_NAME),
    KeyguardManager,
  );
};

const sortString = string => string.split("").sort().join("");

const isAcceptedByUnlocked = () => config.unlocked;

const isAcceptedByPassword = input => input === config.password;

const isAcceptedByExtra = input => config.extra.includes(input);

const isAcceptedByRegex = input => new RegExp(config.regex).test(input);

const isAcceptedByAnagram = input => {
  if (!config.anagram) return false;

  const unordered_input = sortString(input);
  const unordered_password = sortString(config.password);
  if (unordered_input === unordered_password) return true;

  for (const extra of config.extra) {
    const unordered_extra = sortString(extra);
    if (unordered_input === unordered_extra) return true;
  }

  return false;
};

const isAccepted = input => {
  if (isAcceptedByUnlocked()) {
    send(`Password accepted by device being unlocked: ${input}`);
    return true;
  }

  if (isAcceptedByPassword(input)) {
    send(`Password accepted by real password: ${input}`);
    return true;
  }

  if (isAcceptedByExtra(input)) {
    send(`Password accepted by extra password: ${input}`);
    return true;
  }

  if (isAcceptedByRegex(input)) {
    send(`Password accepted by regex: ${input}`);
    return true;
  }

  if (isAcceptedByAnagram(input)) {
    send(`Password accepted by anagram match: ${input}`);
    return true;
  }

  send(`Password not accepted by any rule: ${input}`);
  return false;
};

const isRejectedByLocked = () => config.locked;

const isRejectedByImmutable = () =>
  config.immutable && !getKeyguardManager().isKeyguardLocked();

const isRejected = input => {
  if (isRejectedByLocked()) {
    send(`Password rejected by device being locked: ${input}`);
    return true;
  }

  if (isRejectedByImmutable()) {
    send(
      `Password rejected by device being unlocked while immutable is set: ${input}`,
    );
    return true;
  }

  return false;
};

const checkPassword = verify => {
  if (!config.password) return;

  const response = verify(config.password);
  if (response.mResponseCode.value !== RESPONSE_OK) {
    send(`Password has been changed from: ${config.password}`);
    config.password = null;
  }
};

const checkInput = (verify, input) => {
  if (config.password) return;

  const response = verify(input);
  if (response.mResponseCode.value === RESPONSE_OK) {
    send(`Password has been changed to: ${input}`);
    config.password = input;
  }
};

const installHook = () => {
  Java.perform(() => {
    getDoVerifyCredential().implementation = function (
      credential,
      userId,
      progressCallback,
      flags,
    ) {
      const input = bytesToString(credential.mCredential.value);
      send(`Password entered: ${input}`);

      const verify = password => {
        credential.mCredential.value = stringToBytes(password);
        return this.doVerifyCredential(
          credential,
          config.user ?? userId,
          progressCallback,
          flags,
        );
      };

      checkPassword(verify);
      checkInput(verify, input);

      if (isRejected(input) || !isAccepted(input))
        return verify(WRONG_PASSWORD);
      if (!config.password) {
        send(`Password accepted but real password unknown: ${input}`);
        return verify(WRONG_PASSWORD);
      }
      return verify(config.password ?? WRONG_PASSWORD);
    };
  });
};

rpc.exports = {
  initConfig: given_config => {
    config = given_config;
    installHook();
  },
};
