import Java from "frida-java-bridge";

let actualPassword;
let additionalPasswords;

const LOCK_SETTINGS_SERVICE_CLASS_NAME =
  "com.android.server.locksettings.LockSettingsService";

const string_to_bytes = string =>
  string.split("").map(char => char.charCodeAt(0));

const bytes_to_string = bytes => {
  let out = "";
  for (let i = 0; i < bytes.length; i++) {
    out += String.fromCharCode(bytes[i] & 0xff);
  }
  return out;
};

const isAllowed = password =>
  additionalPasswords.includes(bytes_to_string(password.mCredential.value));

const installHook = () => {
  Java.perform(() => {
    const lockSettingsService = Java.use(LOCK_SETTINGS_SERVICE_CLASS_NAME);

    lockSettingsService.doVerifyCredential.implementation = function (
      credential,
      userId,
      progressCallback,
      flags,
    ) {
      if (isAllowed(credential)) {
        credential.mCredential.value = string_to_bytes(actualPassword);
      }
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
  initConfig: config => {
    actualPassword = config.actualPassword;
    additionalPasswords = config.additionalPasswords;
    installHook();
  },
};
