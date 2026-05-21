import stun

def get_ip_via_stun():
    """
        [辅助函数] 获取本机公网 IP
        注意：在服务器部署时，这获取的是服务器机房 IP。
        如果要获取终端用户 IP，建议使用 ContextVars 从 HTTP Header 中透传。


        stun:帮助你查询你设备网络情况
    """

    try:
        # 默认使用公用的 STUN 服务器
        # external_ip:当前私域ip[192.168.34.39]---->对应的出口ip(公网)---123.120.109.232(地址)
        nat_type, external_ip, external_port = stun.get_ip_info()
        return external_ip
    except Exception as e:
        print(f"STUN 获取失败: {e}")
        return None




if __name__ == '__main__':
    print(get_ip_via_stun())