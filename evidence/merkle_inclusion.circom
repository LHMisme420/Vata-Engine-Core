pragma circom 2.1.6;
include "circomlib/circuits/poseidon.circom";

template MerkleInclusion(depth) {
    signal input leaf;
    signal input siblings[depth];
    signal input pathIndices[depth];
    signal input root;

    signal hashes[depth + 1];
    hashes[0] <== leaf;

    component h[depth];
    component mux0[depth];
    component mux1[depth];

    signal leftInput[depth];
    signal rightInput[depth];

    for (var i = 0; i < depth; i++) {
        // pathIndices[i] == 0 means: current is left, sibling is right
        // pathIndices[i] == 1 means: sibling is left, current is right
        leftInput[i] <== hashes[i] + pathIndices[i] * (siblings[i] - hashes[i]);
        rightInput[i] <== siblings[i] + pathIndices[i] * (hashes[i] - siblings[i]);

        h[i] = Poseidon(2);
        h[i].inputs[0] <== leftInput[i];
        h[i].inputs[1] <== rightInput[i];

        hashes[i + 1] <== h[i].out;
    }

    root === hashes[depth];
}

component main {public [root]} = MerkleInclusion(2);
