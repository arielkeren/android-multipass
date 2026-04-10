const LOCK_SETTINGS_SERVICE_CLASS_NAME =
  "com.android.server.locksettings.LockSettingsService";
const ACTIVITY_THREAD_CLASS_NAME = "android.app.ActivityThread";
const KEYGUARD_MANAGER_CLASS_NAME = "android.app.KeyguardManager";
const VERIFY_CREDENTIAL_RESPONSE_CLASS_NAME =
  "com.android.internal.widget.VerifyCredentialResponse";

const KEYGUARD_SERVICE_NAME = "keyguard";

export default class DeviceController {
  constructor(Java) {
    this.Java = Java;
  }

  getDoVerifyCredential() {
    const LockSettingsService = this.Java.use(LOCK_SETTINGS_SERVICE_CLASS_NAME);
    return LockSettingsService.doVerifyCredential;
  }

  isKeyguardLocked() {
    const ActivityThread = this.Java.use(ACTIVITY_THREAD_CLASS_NAME);
    const currentApplication = ActivityThread.currentApplication();
    const applicationContext = currentApplication.getApplicationContext();
    const keyguardSystemService = applicationContext.getSystemService(
      KEYGUARD_SERVICE_NAME,
    );

    const KeyguardManager = this.Java.use(KEYGUARD_MANAGER_CLASS_NAME);
    const keyguardManager = this.Java.cast(
      keyguardSystemService,
      KeyguardManager,
    );
    return keyguardManager.isKeyguardLocked();
  }

  getResponseOk() {
    const VerifyCredentialResponse = this.Java.use(
      VERIFY_CREDENTIAL_RESPONSE_CLASS_NAME,
    );
    return VerifyCredentialResponse.RESPONSE_OK.value;
  }
}
