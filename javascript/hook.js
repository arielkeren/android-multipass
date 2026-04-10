import Java from "frida-java-bridge";
import injectHook from "./injector";

rpc.exports = {
  initConfig: config => {
    injectHook(Java, config);
  },
};
