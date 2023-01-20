#include "arm/armLib.h"


using namespace arm;

namespace{
    struct LCfg{
    }; LCfg lc_;
    //----
    string enc_json(const ArmSt& st)
    {
        
        string s="{}";
        return s;
    }
}


//-------
ArmCmd::ArmCmd()
{
    sHelp_ = "(robot arm commands)";

    //----
    add("init", mkSp<Cmd>("arm=[z1]",
    [&](CStrs& args)->bool{ 
        return init(args);
    }));
    //----
    add("moveto", mkSp<Cmd>("xyz=x,y,z rvec=rx,ry,rz grip=[0:1]",
    [&](CStrs& args)->bool{ return moveto(args); }));
    //----
    add("st", mkSp<Cmd>("(get status)",
    [&](CStrs& args)->bool{ 
        return getSt();
    }));
  
  
}
//----
bool ArmCmd::init(CStrs& args)
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
bool ArmCmd::checkInit()
{
    if(data_.hasInit) return true;
    log_e("Arm not init");
    return false;
}

//----
bool ArmCmd::moveto(CStrs& args)
{
    if(!checkInit())
        return false;

    assert(p_arm_!=nullptr);
    auto& arm = *p_arm_;

    //----
    StrTbl kv; parseKV(args, kv);
    string sxyz = lookup(kv, string("xyz"));
    string srvec = lookup(kv, string("rvec"));
    string sgrip = lookup(kv, string("grip"));

    //----
    TipSt st;
    
    bool ok = true;
    ok &= st.T.e.parse(srvec);
    ok &= s2v(sxyz, st.T.t);
    ok &= s2d(sgrip, st.gripper);
    if(!ok)
    {
        log_e("Error parsing args");
        return false;
    }
   // log_i("run cmd moveto:"+st.str());

    //---- run
    arm.moveTo(st);

    return true;
}

//----
bool ArmCmd::getSt()
{
    if(p_arm_==nullptr)
        return false;
    ArmSt st;
    bool ok = p_arm_->getSt(st);
    string s = enc_json(st);
    log_i("arm_st:"+s);
    return ok;
}

