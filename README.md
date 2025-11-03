# MSDT: Blockchain-Based Multi-Subset Data Trading Protocol Enabled Data Availability and Non-repudiation

## 论文性能测试

通过在本地搭建私有以太坊区块链来测试论文中设计的智能合约的gas开销

### 安装依赖

运行 `pip install -r requirements.txt` 安装所需的python库

### 搭建私有链

在本地搭建一条以太坊私有链，可以使用truffle的ganache组件快速完成

### 创建账户

创建两个区块链账户并保证账户中余额充足

## 链上gas开销测试

将两个账户地址以及私钥写入 `MSDT\single\wallet\client.json`和 `MSDT\single\wallet\cloud.json`

将本地节点rpc地址写入 `MSDT\single\wallet\rpc.json`

启用私有区块链后，进入single目录，运行 `python gas_test.py`完成合约的gas开销测试
