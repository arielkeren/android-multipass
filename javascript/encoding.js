export const stringToBytes = string =>
  string.split("").map(char => char.charCodeAt(0));

export const bytesToString = bytes => {
  let out = "";
  for (let i = 0; i < bytes.length; i++) {
    out += String.fromCharCode(bytes[i]);
  }
  return out;
};

export const sortString = string => string.split("").sort().join("");
