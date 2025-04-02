import hashlib

def _sha3_256(data):
    return hashlib.sha3_256(data.encode('utf-8')).hexdigest()

def compute_block_hash(prev_block_hash, block_number, merkle_root):
    data = prev_block_hash + str(block_number) + merkle_root
    return _sha3_256(data)

def compute_txn_hash(txn):
    #changed the hashing
    data = txn[0] + str(txn[3]) + txn[1] + str(txn[2])
    return _sha3_256(data)

def compute_merkle_root(transactions):
    if not transactions:
        return _sha3_256("")
    #hashes of each txns
    txn_hashes = [compute_txn_hash(t) for t in transactions]
    #building the tree
    while len(txn_hashes) > 1:
        new_level = []
        i = 0
        while i < len(txn_hashes) - 1:
            concat = txn_hashes[i] + txn_hashes[i+1]
            new_level.append(_sha3_256(concat))
            i+=2
        if len(txn_hashes)%2 == 1:
            new_level.append(_sha3_256(new_level[-1] + txn_hashes[-1]))
        txn_hashes = new_level #now the txn hashes contain the new level of txn hashes after computation of prev
    return txn_hashes[0] #root

def main():
    #input
    num_acc = int(input())
    balances = {}
    for _ in range(num_acc):
        acc, bal = input().split()
        balances[acc]= int(bal)

    num_txn = int(input())
    ogtxns = []
    for _ in range(num_txn):
        from_acc, to_acc, amount, extra = input().split()
        ogtxns.append([from_acc, to_acc, int(amount), int(extra)])
    
    #sorting based on descending incentive and ascending reciever ascii
    txns = sorted(ogtxns, key = lambda x:(-x[3], x[1]))

    #blockchain
    prev_block_hash = '0'
    block_number = 1
    current_block_txns = []

    for txn in txns:
        fro, to, amt, extra_data = txn
        if balances.get(fro, 0) >= amt:
            balances[fro] -= amt
            balances[to] += amt
            current_block_txns.append(txn)
        if len(current_block_txns) == 3 or txn == txns[-1]:
            #Merkle_root
            txn_hashes = [compute_txn_hash(t) for t in current_block_txns]
            merkle_root = compute_merkle_root(txn_hashes)
            #Block hash
            block_hash = compute_block_hash(prev_block_hash, block_number, merkle_root)
            #Output
            print(block_number)
            print(block_hash)
            print(current_block_txns)
            print(merkle_root)

            prev_block_hash = block_hash
            block_number += 1
            current_block_txns = []

if __name__ == "__main__":
    main()