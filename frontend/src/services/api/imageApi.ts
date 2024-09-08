import axios from "axios";

const sendImagePrompt = async (
    prompt: string
) => {
    const data = axios.post(
        `https://9261-2401-4900-8838-6e3d-1b70-8d1e-a8bd-8b4d.ngrok-free.app/api/v1/image/`,
        {
            prompt: prompt
        },
    );
    return data;
}

const sendImageGenerationSignedTx = async (
    signedTx: string
) => {
    axios.post(`https://9261-2401-4900-8838-6e3d-1b70-8d1e-a8bd-8b4d.ngrok-free.app/api/v1/image/generate`, {
        signed_txn: signedTx
    },);
    return;
}

export { sendImagePrompt, sendImageGenerationSignedTx };