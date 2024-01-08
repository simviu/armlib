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
    string sH = "angles=j1,j2,j3,j4,j5,j6 [grip=<GRIP>] [spd=0..1] \n";
    sH += "  angles are degree\n";
    sH += "  GRIP: [open,close] => [0, 1.0]";
    add("setJoints", mkSp<Cmd>(sH,
    [&](CStrs& args)->bool{ return setJoints(args); }));
    
    //----
    add("setGrip", mkSp<Cmd>("grip=<GRIP> [spd=0..1]",
    [&](CStrs& args)->bool{ return setGrip(args); }));
    
    //----
    add("moveto", mkSp<Cmd>("xyz=x,y,z [quat=w,x,y,z] [grip=0...1] [spd=0..1]",
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
    string s_h = "target=<x,y,z>  dt0=<dx,dy,dz> quat=w,x,y,z";
    s_h += "\n      (dt0 is offset for approach point)";
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
bool ArmMng::chkInit()const
{
    if(data_.hasInit && (p_arm_!=nullptr))
        return true;
    log_e("ArmMng arm not init");
    return false;
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
    if(data_.hasInit && (p_arm_!=nullptr))
        return true;

    log_e("Arm not init");
    return false;
}

//----
bool ArmMng::setJoints(CStrs& args)
{
    KeyVals kvs(args);

    //----
    vector<double> as;
    if(!s2data(kvs["angles"], as)) return false;
    
    if(!chkInit())return false;
    auto& arm = *p_arm_;
    
    ArmSt st;
    int i=0;
    st.angles.clear();
    for(auto& a: as)
        st.angles.push_back(a);

    //----
    st.tip.gripper = -1; // -1 for inactive
    string sGrip = kvs["grip"];
    bool ok = true;
    if( sGrip!="")
        ok = s2d(sGrip, st.tip.gripper);
    if(!ok) return false;
    double spd = 1; kvs.get("spd", spd);
    return arm.setJoints(st, spd);
}
//----
bool ArmMng::setGrip(CStrs& args)
{
    KeyVals kvs(args);
    assert(p_arm_!=nullptr);
    auto& arm = *p_arm_;
    
    string sGrip = kvs["grip"];
    double d = -1;
    bool ok = true;
    if( sGrip!="")  
        ok = s2d(sGrip, d);
    if(!ok) return false;    
    double spd = 1; kvs.get("spd", spd);
    return arm.setGrip(d, spd);
}

//----
bool ArmMng::moveto(CStrs& args)
{
    if(!checkInit())
        return false;

    KeyVals kvs(args);

    assert(p_arm_!=nullptr);
    auto& arm = *p_arm_;

    //----
    string sxyz  = kvs["xyz"];
    string sq    = kvs["quat"];
    string sgrip = kvs["grip"];

    //----
    TipSt st;
    bool ok = true;    
    ok &= s2v(sxyz, st.T.t);
    if(!ok)
    {
        log_e("Error parsing args");
        return false;
    }
    //---
    // option
    st.gripper = -1;
    if(sgrip!="")
        ok &= s2d(sgrip, st.gripper);

    if(sq!="")
        ok &=s2q(sq, st.T.q); 
    double spd = 1; kvs.get("spd", spd);
    //----
    if(!ok)
    {
        log_e("parsing fail");
        return false;
    }

    //---- run
    return arm.moveTo(st, spd);

}

//---
bool ArmMng::grab(CStrs& args)
{
    if(!checkInit())
        return false;

    StrTbl kv; parseKV(args, kv);
    Trans Tt;
    vec3 dt0;
    bool ok = true;
    ok &= s2v(lookup(kv, "target"), Tt.t);
    ok &= s2v(lookup(kv, "dt0"), dt0);
    quat q;
    ok &= s2q(lookup(kv, "quat"), q);
    if(!ok){ log_e("syntax err"); return false; }
    Tt.q = q;
    assert(p_arm_!=nullptr);
    return p_arm_->grab(Tt, dt0);    
}

//----
bool ArmMng::getSt()
{
    string s;
    if(p_arm_==nullptr)
    {
        sRes_ = "arm not init";
        return false;
    }
    //----
    ArmSt st;
    if(p_arm_->getSt(st))
        s = st.str();
    else
        s = "fail to call arm getSt()";
    
    log_i("arm_st:"+s);
    sRes_ = s;
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
