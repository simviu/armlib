#include "arm/armTcp.h"
#include "json/json.h"

using namespace arm;

namespace{
     
    //----
    bool decSt_json(const Json::Value& jd, 
                    ArmSt& st)
    {

        auto& jtip = jd["tip"];
        auto& tip = st.tip;
        bool ok = true;
        //--- options
        auto& jT = jtip["T"];
        auto& T = tip.T;
        ok &= s2v(jT["t"].asString(), T.t);
        ok &= T.e.set(jT["e"].asString());
        return ok;
    }
    //---- decSt
    bool decSt(const string& sln, ArmSt& st)
    {
        bool ok = true;
        //---- decode json
        try{
            Json::Reader rdr;
            Json::Value jd;
            rdr.parse(sln, jd);
            ok &= jd["ok"].asBool();
            if(ok)
                ok &= decSt_json(jd["res"]["st"], st);
        }
        catch(exception& e)
        {
            log_e("exception caught:"+string(e.what()));
            ok = false;
        }        
        return true;
    }
}

//----

ArmTcp::ArmTcp(const string& sHost, int port)
{
    auto& cntx = client_.cntx_;
    cntx.sHost = sHost;
    cntx.port = port;
}

ArmTcp::ArmTcp(const string& sUri)
{
    auto ss = tokens(sUri, ':');
    if(ss.size()<2)
    {
        log_e("sUri incorrect:'"+sUri+
        "', expect 'ip/hostname:port'");
        return;
    }
    //----
    client_.cntx_.sHost = ss[0];
    s2d(ss[1], client_.cntx_.port);
}

//-----
bool ArmTcp::init()
{
    auto& cntx = client_.cntx_;

    bool ok = client_.connect(cntx.sHost, cntx.port); 
    //--- deprecated
    /*
    thd_ = std::thread([&](){
        while(ok)
        {
            ok = run_once();
            sys::sleep(1.0/cfg_.fps_st);
        }
        //---- disconnected or error
        log_i("ArmTcp client disconnected or failed");
    });
    thd_.detach();
    */
    return ok;
}
//----
/*
bool ArmTcp::run_once()
{
    std::unique_lock<std::mutex> lock(thd_mtx_);
    bool ok = true;
    ok &= send_cmds();
    ok &= read_st();
    return ok;
}
*/
//----
bool ArmTcp::read_st()    
{   
    //log_d("read_st()...");
    client_.send("st");
    string sln;
    if(!client_.recvLn(sln)) {
        log_d("read_st failed");
        return false;
    }
    log_d("read_st() recv:["+sln+"]");
    //----
    ArmSt st;
    if(!decSt(sln, st))
    {
        log_e("read_st() json err");
        return false;
    }
    //---- fill st
    std::unique_lock<std::mutex> lk(mtx_st_);
    data_.cur_st = st;
    data_.b_st_val = true;
    log_d("ArmTcp read_st() cur_st ok, tip at:"+str(st.tip.T.t));
    return true;
}

//---- deprecated, switch to blocking mode
/*
bool ArmTcp::send_cmds()    
{   
    //log_d("ArmTcp send_cmds()...");
    auto& cmds = data_.cmds;
    
    while(cmds.size()>0)
    {
        string scmd = cmds.pop();
        if(scmd=="")continue;
        //log_d("armTcp sending cmd:'"+scmd+"'");
        
        if(!client_.send(scmd+"\n"))
        {
            log_e("AmrTcp send_cmds fail");
            return false;
        }
        //----
        string sln;
        if(!client_.recvLn(sln))
        {
            log_e("ArmTcp read cmd ack fail");
            return false;
        }
    }
    return true;

}
*/
//----
bool ArmTcp::init_arm(const string& sModel)
{
    return send("init arm="+sModel);
}
//--- blocking mode
bool ArmTcp::send(const string& scmd)
{  
    if(!client_.send(scmd+"\n"))
    {
        log_e("ArmTcp send cmd fail");
        return false;
    }
    log_d("  wait ack...");
    //--- receive ack
    Cmd::Ack ack;
    if(!getAck(ack)) return false;
    return true;
}
//----
bool ArmTcp::getAck(Cmd::Ack& ack)
{
    vector<string> sLns;
    while(1)
    {
        string sr;
        if(!client_.recvLn(sr))
        {
            log_e("ArmTcp recv ack fail");
            return false;
        }
        //
        string s = ut::remove(sr, '\n');
        log_d("recv ln:'"+s+"'");
        sLns.push_back(s);
        if(s=="cmd_ack_end")break;
        //----
    }
    //---- decode
    if(!ack.dec(sLns)) 
        return false;
    log_i("ArmTcp recv ack:");
    log_i(ack.str());
    return true;
}

//----
bool ArmTcp::release()
{
    return client_.send("release");
}

//---
bool ArmTcp::reset()
{
    return client_.send("reset");

}

//-----
bool ArmTcp::moveTo(const TipSt& ts, float spd) 
{
    string s = "moveto ";

    s += "xyz=" + remove(str(ts.T.t), ' ') + " ";
    s += "rvec=" + remove(ts.T.e.str(), ' ') + " ";
    s += "grip=" + str(ts.gripper) +" ";

    float spdm = Arm::cfg_.maxSpeed;
    s += "spd=" + str(std::max(spd, spdm));

    //bool ok = client_.send(s);
    return send(s);

}

bool ArmTcp::getSt(ArmSt& st)
{
    std::unique_lock<std::mutex> lk(mtx_st_);
    st = data_.cur_st;
    return data_.b_st_val;
}

bool ArmTcp::test()
{
    return true;

}

//----
bool ArmTcp::setJoints(const ArmSt& st, double t)
{
    return true; 
}
