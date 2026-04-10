import DeviceController from "./device_controller";
import CredentialUpdater from "./credential_updater";
import CredentialChecker from "./credential_checker";
import { bytesToString, stringToBytes } from "./encoding.js";

const WRONG_PASSWORD = "0";

const injectHook = (Java, config) => {
  Java.perform(() => {
    const deviceController = new DeviceController(Java);
    const credentialUpdater = new CredentialUpdater(config);
    const credentialChecker = new CredentialChecker(config, deviceController);

    deviceController.getDoVerifyCredential().implementation = function (
      credential,
      userId,
      progressCallback,
      flags,
    ) {
      const input = bytesToString(credential.mCredential.value);
      send(`Password entered: ${input}`);

      const verify = (password, shouldInform) => {
        credential.mCredential.value = stringToBytes(password);
        return this.doVerifyCredential(
          credential,
          config.user ?? userId,
          shouldInform ? progressCallback : null,
          flags,
        );
      };
      const check = password =>
        verify(password, false).mResponseCode.value ===
        deviceController.getResponseOk();
      const reject = () => verify(WRONG_PASSWORD, true);

      credentialUpdater.updatePassword(check);
      credentialUpdater.updateInput(check, input);

      if (
        credentialChecker.isRejected(input) ||
        !credentialChecker.isAccepted(input)
      )
        return reject();
      if (!config.password) {
        send(`Password accepted but real password unknown: ${input}`);
        return reject();
      }
      return verify(config.password, true);
    };
  });
};

export default injectHook;
