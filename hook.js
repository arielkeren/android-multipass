import Java from "frida-java-bridge";

let config;

const LOCK_SETTINGS_SERVICE_CLASS_NAME =
  "com.android.server.locksettings.LockSettingsService";

const stringToBytes = string =>
  string.split("").map(char => char.charCodeAt(0));

const bytesToString = bytes => {
  let out = "";
  for (let i = 0; i < bytes.length; i++) {
    out += String.fromCharCode(bytes[i]);
  }
  return out;
};

const sortString = string => string.split("").sort().join("");

const isAcceptedByDisable = _ => config.disable;

const isAcceptedByPassword = input => input === config.password;

const isAcceptedByAdditional = input => config.additional.includes(input);

const isAcceptedByRegex = input => new RegExp(config.regex).test(input);

const isAcceptedByUnordered = input => {
  const unordered_input = sortString(input);
  const unordered_password = sortString(config.password);
  if (unordered_input === unordered_password) return true;

  for (const additional of config.additional) {
    const unordered_additional = sortString(additional);
    if (unordered_input === unordered_additional) return true;
  }

  return false;
};

const isAccepted = input => {
  if (isAcceptedByDisable(input)) {
    send(`Password accepted by verification being disabled: ${input}`);
    return true;
  }

  if (isAcceptedByPassword(input)) {
    send(`Password accepted by real password: ${input}`);
    return true;
  }

  if (isAcceptedByAdditional(input)) {
    send(`Password accepted by additional password: ${input}`);
    return true;
  }

  if (isAcceptedByRegex(input)) {
    send(`Password accepted by regex: ${input}`);
    return true;
  }

  if (isAcceptedByUnordered(input)) {
    send(`Password accepted by unordered character match: ${input}`);
    return true;
  }

  return false;
};

const installHook = () => {
  Java.perform(() => {
    const lockSettingsService = Java.use(LOCK_SETTINGS_SERVICE_CLASS_NAME);

    lockSettingsService.doVerifyCredential.implementation = function (
      credential,
      userId,
      progressCallback,
      flags,
    ) {
      const input = bytesToString(credential.mCredential.value);
      send(`Password entered: ${input}`);

      if (isAccepted(input))
        credential.mCredential.value = stringToBytes(config.password);
      else send(`Password rejected: ${input}`);

      return this.doVerifyCredential(
        credential,
        userId,
        progressCallback,
        flags,
      );
    };
  });
};

rpc.exports = {
  initConfig: given_config => {
    config = given_config;
    installHook();
  },
};
