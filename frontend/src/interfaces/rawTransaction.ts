import { AddressLike } from "ethers";
import { BigNumberish } from "ethers";

interface rawTransaction {
    nonce: number | null | undefined,
    gasLimit: BigNumberish | null | undefined,
    gasPrice: number | null | undefined,
    to: AddressLike,
    value: BigNumberish | null | undefined,
    data: string | null | undefined,
}

export default rawTransaction;
