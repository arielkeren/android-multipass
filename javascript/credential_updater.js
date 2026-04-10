export default class CredentialUpdater {
  constructor(config) {
    this.config = config;
  }

  updatePassword(check) {
    if (this.config.password && !check(this.config.password)) {
      send(`Password has been changed from: ${this.config.password}`);
      this.config.password = null;
    }
  }

  updateInput(check, input) {
    if (!this.config.password && check(input)) {
      send(`Password has been changed to: ${input}`);
      this.config.password = input;
    }
  }
}
