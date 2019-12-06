// 使用嚴格模式
"use strict";

{

  var rsa_encrypt = (data, object, public_key_id, key_id) => {
    const data_string = JSON.stringify(data);
    const key = $('#' + object);
    const public_key = key.data(public_key_id);
    const id = key.data(key_id);
    // 公鑰物件
    const public_key_obj = forge.pki.publicKeyFromPem(public_key);

    // 前端使用者瀏覽器加密
    let encrypted = public_key_obj.encrypt(data_string, "RSA-OAEP", {
      md: forge.md.sha256.create(),
      mgf1: forge.mgf1.create()
    });

    // 編碼成base64
    let base64 = forge.util.encode64(encrypted);

    return [id, base64];
  }

  //rsa_encrypt({ 'tai': 10 }, 'rsa-key', 'public-key', 'key-id');
}


