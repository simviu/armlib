#include "arm/armLib.h"
#include "arm/armTcp.h"


using namespace arm;

namespace{
    struct LCfg{
    }; LCfg lc_;
    
}


//-------
ArmMng::ArmMng()
{
    init_cmds();
    

}

//----
void ArmMng::init_cmds()
{
    sHelp_ = "(robot arm commands)";

    //----
    add("init", mkSp<Cmd>("arm=[z1]",
    [&](CStrs& args)->bool{ 
        return init(args);
    }));
    //----
    add("client", mkSp<Cmd>("host=<HOST> port=<PORT> arm=[z1]",
    [&](CStrs& args)->bool{ 
        return client(args);
    }));
    //----
    add("moveto", mkSp<Cmd>("xyz=x,y,z [euler=rx,ry,rz] [grip=0...1]",
    [&](CStrs& args)->bool{ return moveto(args); }));
    //----
    add("st", mkSp<Cmd>("(get status)",
    [&](CStrs& args)->bool{ 
        return getSt();
    }));
    //----
    add("play", mkSp<Cmd>("name=<LABEL_NAME> ",
    [&](CStrs& args)->bool{ 
        StrTbl kv; parseKV(args, kv);
        return play(lookup(kv, "name"));
    }));
    //----
    string s_h = "target=<x,y,z>  dT0=<dx,dy,dz> euler=rx,ry,rz";
    s_h += "\n      (dT0 is offset for approach point)";
    add("grab", mkSp<Cmd>(s_h,
    [&](CStrs& args)->bool{ return grab(args);  }));
  
  
}
//----
bool ArmMng::init(CStrs& args)
{
    data_.hasInit = false;

    StrTbl kv; parseKV(args, kv);
    string sN = lookup(kv, "arm");
    if(sN=="")
    {
        log_e("Missing or empty arg arm=''");
        return false;
    }
    auto p = Arm::create(sN);
    if(p==nullptr)
    {
        log_e("Arm create failed:'"+sN+"'");
        return false;
    }
    bool ok = p->init();
    if(!ok) {
        log_e("Arm init failed:'"+sN+"'");
        return false;
    }

    log_i("Arm init ok : '"+sN+"'");
    p_arm_ = p;
    data_.hasInit = true;
    return true;
}
//----
bool ArmMng::client(CStrs& args)
{
    data_.hasInit = false;

    KeyVals kvs(args);
    string sHost, sArm; int port=-1;
    bool ok = kvs.get("host", sHost) &&
              kvs.get("port", port) &&
              kvs.get("arm", sArm);
    
    if(!ok)
    {
        log_e("fail to get host, port, or arm");
        return false;
    }
    //----
    auto p = mkSp<ArmTcp>(sHost, port);
    if(p==nullptr)
    {
        log_e("failed create client ");
        return false;
    }

    //---- init
    ok &= p->init();
    sys::sleep(0.01);
    ok &= p->init_arm(sArm);
    if(!ok) {
        log_e("Arm init failed");
        return false;
    }
    sys::sleep(1);

    //----
    stringstream s;
    s << "Arm client connect ok, " << sHost;
    s << ":" << port;
    log_i(s.str());
    p_arm_ = p;
    data_.hasInit = true;
    return true;
}

//----
bool ArmMng::checkInit()
{
    if(data_.hasInit) return true;
    log_e("Arm not init");
    return false;
}

//----
bool ArmMng::moveto(CStrs& args)
{
    if(!checkInit())
        return false;

    assert(p_arm_!=nullptr);
    auto& arm = *p_arm_;

    //----
    StrTbl kv; parseKV(args, kv);
    string sxyz = lookup(kv, string("xyz"));
    string se = lookup(kv, string("euler"));
    string sgrip = lookup(kv, string("grip"));

    //----
    TipSt st;
    
    bool ok = true;
    
    ok &= s2v(sxyz, st.T.t);
    if(!ok)
    {
        log_e("Error parsing args");
        return false;
    }

    // option
    if(sgrip!="")
        s2d(sgrip, st.gripper);
    if(se!="")
        st.T.e.set(se);
   // log_i("run cmd moveto:"+st.str());

    //---- run
    return arm.moveTo(st);

}

//---
bool ArmMng::grab(CStrs& args)
{
    if(!checkInit())
        return false;

    StrTbl kv; parseKV(args, kv);
    Trans Tt, Tc;
    bool ok = true;
    ok &= s2v(lookup(kv, "target"), Tt.t);
    ok &= s2v(lookup(kv, "dt0"), Tc.t);
    Euler e;
    ok &= e.set(lookup(kv, "euler"));
    if(!ok){ log_e("syntax err"); return false; }
    Tt.e = Tc.e = e;
    assert(p_arm_!=nullptr);
    return p_arm_->grab(Tt, Tc);    
}

//----
bool ArmMng::getSt()
{
    string s;
    if(p_arm_==nullptr)
        s = "arm not init";

    ArmSt st;
    if(p_arm_->getSt(st))
        s = st.str();
    else
        s = "fail to call arm getSt()";
    
    log_i("arm_st:"+s);
    return true;
}

//----
bool ArmMng::play(const string& sf)
{
    if(!checkInit())
        return false;
    assert(p_arm_!=nullptr);
    return p_arm_->play(sf);
}
