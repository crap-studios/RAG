import axios from "axios";
import rawTransaction from "../../interfaces/rawTransaction";

const sendImagePrompt = async (
    prompt: string
) => {
    const data = await axios.post(
        `https://9261-2401-4900-8838-6e3d-1b70-8d1e-a8bd-8b4d.ngrok-free.app/api/v1/image/`,
        {
            prompt: prompt
        },
        {
            headers: {
                'Authorization': "Bearer " + localStorage.getItem("accessToken")
            },
        }
    );
    const rawTxJSON = data.data["data"]["rawTx"];
    const rawTx: rawTransaction = {
        nonce: rawTxJSON["nonce"],
        gasLimit: rawTxJSON["gasLimit"],
        gasPrice: rawTxJSON["gasPrice"],
        to: rawTxJSON["to"],
        value: rawTxJSON["value"],
        data: rawTxJSON["data"],
    }
    return rawTx;
}

const sendImageGenerationSignedTx = async (
    signedTx: string
) => {
    axios.post(`https://9261-2401-4900-8838-6e3d-1b70-8d1e-a8bd-8b4d.ngrok-free.app/api/v1/image/generate`, {
        signed_txn: signedTx
    }, {
        headers: {
            'Authorization': "Bearer " + localStorage.getItem("accessToken")
        },
    });
    return;
}

export { sendImagePrompt, sendImageGenerationSignedTx };