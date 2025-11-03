pragma solidity ^0.6.0;

contract Launchpad{
    // uint constant _n = 1;
    uint _n;
    
    address private _cloud; 
    
    // address private _client;
    
    uint256 private _cloudPenalty;
    
    uint256 private _clientServiceFee;
    
    // int private _serviceStatus;
    
    bytes32[] private _verifyResult;
    
    uint256 private _duringTime;
    
    // uint256 private _requestStartTime;
    
    string private _serviceName;
    
    uint private _randomBlock;
    
    // uint8[] private _setSeq;

    // uint private _payNum;

    uint private _isInit;

    // bytes32 private _payHash;

    struct userState{
        address _client;
        uint8[] _setSeq;
        uint _payNum;
        bytes32  _payHash;
        int _serviceStatus;
        uint256 _requestStartTime;
    }

    mapping (string => userState) public stateMap;
    /**
    * @dev Emitted Received money sources  
    *
    */
    event Received(string from, uint256 value);
    
    /**
    * @dev Emitted that cloud initializes the service information and transfer penalty
    *
    */
    event CloudInit(string ret);

    /**
    * @dev Emitted that client requests the service and transfer service fees
    *
    */
    event RequestService(string ret);
    
    /**
    * @dev Emitted that client terminate the service and transfer the service fees
    *
    */
    event CloudTerminate(string ret);
    
    /**
    * @dev Emitted that cloud get the payment by arbitration
    *
    */
    event CloudArbitrate(string ret);
  
    /**
    * @dev Emitted that client terminates the service if cloud didn't terminate the service
    */
    event ClientTerminate(string ret);
    


    constructor(
        uint256 cloudPenalty,
        uint256 clientServiceFee,
        uint256 duringTime,
        uint256 n
    ) 
    public 
    {
        _cloud = msg.sender;
        
        _cloudPenalty = cloudPenalty;

        _clientServiceFee = clientServiceFee;
        
        _duringTime = duringTime;
        
        // _requestStartTime = 0;
        
        // _serviceStatus = -1;

        _isInit = 0;

        _n = n;
    }
    
 
    
    /**
    * @dev Function to get details of project
    */
    function getBasicInfos() public view returns (
        address cloud,
        uint256 cloudPenalty,
        uint256 clientServiceFee
    ) {
        cloud = _cloud;
        cloudPenalty = _cloudPenalty;
        clientServiceFee = _n * _clientServiceFee;
    }
    
    function getDetailsInfos() public view returns (
        string memory serviceName,
        bytes32[] memory verifyResult,
        // uint256 requestStartTime,
        uint256 duringTime,
        // int serviceStatus,
        uint256 randomBlock
    ) {
        serviceName = _serviceName;
        verifyResult = _verifyResult;
        // requestStartTime = _requestStartTime;
        duringTime = _duringTime;
        // serviceStatus = _serviceStatus;
        randomBlock = _randomBlock;
    }
    

    
    /**
    * cloud publishes the verify result and transfer penatly
    *
    */
    function cloudInit(bytes32[] memory verifyResult) payable public {
        require(msg.sender == _cloud, "Should be the correct cloud address");
        require(_isInit == 0, "Already initialized");
        require(msg.value == _cloudPenalty, 'Error penatly amount');
            
        address(this).transfer(msg.value);
       
        _verifyResult = verifyResult;
        _isInit = 1;
        // _serviceStatus = 0;
        emit CloudInit("Cloud initialize");
    }

    /**
    * @dev Client requests the service
    *
    */
    function requestService(string memory userid, uint8[] memory setSeq, uint payNum, bytes32 payHash) payable public {
        require(stateMap[userid]._serviceStatus != 1 , "Service already started or finished");
        require(msg.value == payNum * _clientServiceFee, 'Error service fees');
        userState memory user = userState(msg.sender,setSeq,payNum,payHash,1,now);
        stateMap[userid] = user;
        // stateMap[userid]._client = msg.sender;
        // stateMap[userid]._setSeq = setSeq;
        // stateMap[userid]._payNum = payNum;
        // stateMap[userid]._payHash = payHash;
        // stateMap[userid]._serviceStatus = 1;
        // stateMap[userid]._requestStartTime = now;
        address(this).transfer(msg.value);
        emit RequestService("Client Requests Service");
    }    
    
    /**
    * client provide payment seed and transfer the service fees
    *
    */
    function cloudTerminate(string memory userid, bytes32 paySeed, uint setNum) public {
        require(msg.sender == _cloud, "Should be the correct client address");
        require(stateMap[userid]._serviceStatus == 1, "Error service sequence");
        require(now <= stateMap[userid]._requestStartTime + _duringTime, 'The terminate time is over');
        
        for (uint i = 1; i <= setNum; i++) {
            paySeed = sha256(abi.encodePacked(paySeed));
        }
        require(stateMap[userid]._payHash == paySeed, "Error payment seed");
        payable(_cloud).transfer(setNum * _clientServiceFee);
        payable(stateMap[userid]._client).transfer((stateMap[userid]._payNum - setNum) * _clientServiceFee);
        stateMap[userid]._serviceStatus = 2;
        emit CloudTerminate("Cloud terminate");
    }


    function ecrecovery(bytes32 hash, bytes memory sig) pure public returns (address) {
        bytes32 r;
        bytes32 s;
        uint8 v;
        assembly {
        r := mload(add(sig, 32))
        s := mload(add(sig, 64))
        v := and(mload(add(sig, 65)), 255)
        }
        if (v < 27) {
        v += 27;
        }
        return ecrecover(hash, v, r, s);
    }
    /**
    * client provide payment seed and transfer the service fees
    *
    */
    function cloudArbitrate(string memory userid, string memory s2, bytes32 hashOfS1, bytes memory sig, uint setNum, bytes32 newResult) public {
        require(msg.sender == _cloud, "Should be the correct client address");
        require(stateMap[userid]._serviceStatus == 1, "Error service sequence");
        require(now <= stateMap[userid]._requestStartTime + _duringTime, 'The terminate time is over');
        uint n = stateMap[userid]._setSeq[(setNum - 1) % _n] % _n;
        require((hashOfS1 ^ sha256(bytes(s2))) == _verifyResult[n], "Arbitrate fail");
        require(stateMap[userid]._client == ecrecovery(hashOfS1,sig), "Wrong signature");
        _verifyResult[n] = newResult;
        payable(_cloud).transfer(setNum * _clientServiceFee);
        payable(stateMap[userid]._client).transfer((stateMap[userid]._payNum - setNum) * _clientServiceFee);
        stateMap[userid]._serviceStatus = 2;
        emit CloudArbitrate("Cloud arbitrate");
    }    
    
    /**
    *  Client terminates the service if cloud does not terminate service in time.
    */
    function clientTerminate(string memory userid) public {
        require(msg.sender == stateMap[userid]._client, "Should be the correct address");
        require(stateMap[userid]._serviceStatus == 1, "Error service sequence");
        require(now >= stateMap[userid]._requestStartTime + _duringTime, 'The terminate time is not over');
            
        stateMap[userid]._serviceStatus = 2;
        payable(stateMap[userid]._client).transfer(stateMap[userid]._payNum * _clientServiceFee);
        emit ClientTerminate("Client Terminate Service");
    }
       
    function getRandomBlock() view public returns(uint256) {
        return _randomBlock;
    }
    
    function getVerifyResult(uint num) view public returns(bytes32) {
        return _verifyResult[num];
    }
    
    
    function getBalance() view public returns(uint) {
        return address(this).balance;
    }
    
    /**
    * @dev Receive cloud's penatly or client's service fees.
    */
    receive() external payable {
    }
   
}