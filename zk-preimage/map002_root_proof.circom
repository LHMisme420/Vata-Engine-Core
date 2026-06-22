pragma circom 2.0.0;
include "circomlib/circuits/poseidon.circom";

template MerkleRootPreimageProof() {
    signal input root_high;
    signal input root_low;
    signal output hash;
    component poseidon = Poseidon(2);
    poseidon.inputs[0] <== root_high;
    poseidon.inputs[1] <== root_low;
    hash <== poseidon.out;
}
component main = MerkleRootPreimageProof();