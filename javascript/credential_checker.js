import { sortString } from "./encoding.js";

export default class CredentialChecker {
  constructor(config, deviceController) {
    this.config = config;
    this.deviceController = deviceController;
  }

  isAcceptedByUnlocked() {
    return this.config.unlocked;
  }

  isAcceptedByPassword(input) {
    return input === this.config.password;
  }

  isAcceptedByExtra(input) {
    return this.config.extra.includes(input);
  }

  isAcceptedByRegex(input) {
    return new RegExp(this.config.regex).test(input);
  }

  isAcceptedByAnagram(input) {
    if (!this.config.anagram) return false;

    const unordered_input = sortString(input);
    const unordered_password = sortString(this.config.password);
    if (unordered_input === unordered_password) return true;

    for (const extra of this.config.extra) {
      const unordered_extra = sortString(extra);
      if (unordered_input === unordered_extra) return true;
    }

    return false;
  }

  isAccepted(input) {
    if (this.isAcceptedByUnlocked()) {
      send(`Password accepted by device being unlocked: ${input}`);
      return true;
    }

    if (this.isAcceptedByPassword(input)) {
      send(`Password accepted by real password: ${input}`);
      return true;
    }

    if (this.isAcceptedByExtra(input)) {
      send(`Password accepted by extra password: ${input}`);
      return true;
    }

    if (this.isAcceptedByRegex(input)) {
      send(`Password accepted by regex: ${input}`);
      return true;
    }

    if (this.isAcceptedByAnagram(input)) {
      send(`Password accepted by anagram match: ${input}`);
      return true;
    }

    send(`Password not accepted by any rule: ${input}`);
    return false;
  }

  isRejectedByLocked() {
    return this.config.locked;
  }

  isRejectedByImmutable() {
    return (
      this.config.immutable &&
      !this.deviceController.getKeyguardManager().isKeyguardLocked()
    );
  }

  isRejected(input) {
    if (this.isRejectedByLocked()) {
      send(`Password rejected by device being locked: ${input}`);
      return true;
    }

    if (this.isRejectedByImmutable()) {
      send(
        `Password rejected by device being unlocked while immutable is set: ${input}`,
      );
      return true;
    }

    return false;
  }
}
