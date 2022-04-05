pragma solidity ^0.8.0;

contract ShrimpCoin {

    mapping (address => uint) balances;

    constructor() public {
        balances[msg.sender] = 10000;
    }

    function transfer(address receiver, uint amount) public returns(bool sufficient) {
        if (balances[msg.sender] >= amount)
            return false;

        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        return true;
    }

    function get_balance(address account) public view returns(uint) {
        return balances[account];
    }

}
