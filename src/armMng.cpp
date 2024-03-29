#include "arm/armLib.h"


using namespace arm;

namespace{
    struct LCfg{
    }; LCfg lc_;
    
}


//-------
ArmMng::ArmMng()
{
    sHelp_ = "(robot arm commands)";

    //----
    add("init", mkSp<Cmd>("arm=[z1]",
    [&](CStrs& args)->bool{ 
        return init(args);
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
    if(p_arm_==nullptr)
        return false;
    ArmSt st;
    bool ok = p_arm_->getSt(st);
    log_i("arm_st:"+st.str());
    return ok;
}

//----
bool ArmMng::play(const string& sf)
{
    if(!checkInit())
        return false;
    assert(p_arm_!=nullptr);
    return p_arm_->play(sf);
}
