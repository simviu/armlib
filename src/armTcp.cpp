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
        ok &= T.e.parse(jT["e"].asString());
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

            ok &= decSt_json(jd["st"], st);
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
    //---
    thd_ = std::thread([&](){
        while(1)
        {
            read_st();
            send_cmds();
            sys::sleep(1.0/cfg_.fps_st);
        }
    });
    thd_.detach();

    return ok;
}

//----
void ArmTcp::read_st()    
{   
    log_d("read_st()...");
    client_.send("st");
    string sln;
    if(!client_.readLn(sln)) {
        log_d("read_st failed");
        return;
    }
    log_d("read_st() recv:["+sln+"]");
    //----
    ArmSt st;
    if(!decSt(sln, st))
    {
        log_e("read_st() json err");
        return;
    }
    //---- fill st
    std::unique_lock<std::mutex> lk(mtx_st_);
    data_.cur_st = st;


}

//----
void ArmTcp::send_cmds()    
{   
    log_d("ArmTcp send_cmds()...");
    auto& cmds = data_.cmds;
    
    while(cmds.size()>0)
    {
        string scmd = cmds.pop();
        log_d("armTcp sending cmd:'"+scmd+"'");
        
        if(!client_.send(scmd+"\n"))
        {
            log_e("AmrTcp send_cmds fail");
            return;
        }
        //----
        string sln;
        if(!client_.readLn(sln))
        {
            log_e("ArmTcp read cmd ack fail");
            return;
        }
    }

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
    data_.cmds.push(s);
    return true;

}

bool ArmTcp::getSt(ArmSt& st)
{
    std::unique_lock<std::mutex> lk(mtx_st_);
    st = data_.cur_st;
    return true;
}

bool ArmTcp::test()
{
    return true;

}