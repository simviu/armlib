#include "arm/armTcp.h"
#include "json/json.h"

using namespace arm;

namespace{
    // TODO : fix hack for ArmTcp::getSt() const
    std::mutex mtx_; 
    //----
    bool decSt(const Json::Value& jd, 
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
    client_.setRcv([&](const char* buf, int len){
        onRecv(buf, len);
    });
    bool ok = client_.connect(cntx.sHost, cntx.port); 
    return ok;
}

//----
void ArmTcp::onRecv(const char* buf, int len)
{
    string s(buf, len);
    log_d("socket recv:"+s);
    bool ok = true;
    mtx_.unlock();
    //---- decode json
    try{
        Json::Reader rdr;
        Json::Value jd;
        ok &= decSt(jd["st"], data_.cur_st);
    }
    catch(exception& e)
    {
        log_e("exception caught:"+string(e.what()));
        ok = false;
    }
    mtx_.unlock();
    //---
    if(!ok)
        log_e("Recv json err");
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
    mtx_.lock();
    string s = "moveto ";

    s += "xyz=" + remove(str(ts.T.t), ' ') + " ";
    s += "rvec=" + remove(ts.T.e.str(), ' ') + " ";
    s += "grip=" + str(ts.gripper) +" ";
    s += "spd=" + str(std::max(spd, cfg_.maxSpeed));

    bool ok = client_.send(s);
    mtx_.unlock();
    return ok;

}

ArmSt ArmTcp::getSt() const
{
    mtx_.lock();
    ArmSt st = data_.cur_st;
    mtx_.unlock();
    return st;
}

bool ArmTcp::test()
{
    return true;

}