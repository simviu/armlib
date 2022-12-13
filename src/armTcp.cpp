#include "arm/armTcp.h"
#include "json/json.h"

using namespace arm;

namespace{
     
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

    bool ok = client_.connect(cntx.sHost, cntx.port); 
    //---
    st_thd_ = std::thread([&](){
        while(1)
        {
            read_st();
            sys::sleep(1.0/cfg_.fps_st);
        }
    });
    st_thd_.detach();

    return ok;
}

//----
void ArmTcp::read_st()    
{   
    mtx_.lock();
 
    client_.send("st");
    string sln;
    if(!client_.readLn(sln))
        return;
    //----
    bool ok = true;
    //---- decode json
    try{
        Json::Reader rdr;
        Json::Value jd;
        rdr.parse(sln, jd);

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

    float spdm = Arm::cfg_.maxSpeed;
    s += "spd=" + str(std::max(spd, spdm));

    bool ok = client_.send(s);
    mtx_.unlock();
    return ok;

}

bool ArmTcp::getSt(ArmSt& st)
{
    mtx_.lock();
    st = data_.cur_st;
    mtx_.unlock();
    return true;
}

bool ArmTcp::test()
{
    return true;

}