pragma solidity ^0.8.0;

contract ShrimpCoin {

    mapping (address => uint) balances;

    event Transfer(address indexed _from, address indexed _to, uint _value);    // ver 0.2

    constructor() {
        balances[msg.sender] = 10000;
    }

    function transfer(address receiver, uint amount) public returns(bool) {
        if (balances[msg.sender] < amount)
            return false;

        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        emit Transfer(msg.sender, receiver, amount);    // ver 0.2
        return true;
    }

    function get_balance(address account) public view returns(uint) {
        return balances[account];
    }

}
