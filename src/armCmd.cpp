#include "arm/armLib.h"


using namespace arm;

namespace{
    struct LCfg{
    }; LCfg lc_;
    //----
    string enc_json(const ArmSt& st)
    {
        
        string s;
        return s;
    }
}


//-------
ArmCmd::ArmCmd()
{
    

    //----
    add("init", mkSp<Cmd>("init name=[NAME]",
    [&](CStrs& args)->bool{ 
        StrTbl kv; parseKV(args, kv);
        string sN = lookup(kv, "arm");
        p_arm_ = Arm::create(sN);
        if(p_arm_==nullptr)
            return false;
        return p_arm_->init();

    }));
    //----
    add("moveto", mkSp<Cmd>("moveto <x,y,z,rx,ry,rz>",
    [&](CStrs& args)->bool{ return moveto(args); }));
    //----
    add("st", mkSp<Cmd>("(get status)",
    [&](CStrs& args)->bool{ 
        return getSt();
    }));
    //----s
    add("server", mkSp<Cmd>("server port=PORT",
    [&](CStrs& args)->bool{ return run_server(args); }));
    
}
//----
bool ArmCmd::checkInit(CStrs& args)
{
    if(p_arm_!=nullptr)
        return true;
    
    StrTbl kv; parseKV(args, kv);
    string sArm = lookup(kv, "arm");
    if(sArm=="")
        p_arm_ = Arm::create(sArm);
    if(p_arm_==nullptr) {
        log_e("Arm null");
        return false;
    }

    bool ok = p_arm_->init();
    return ok;  
}

//----
bool ArmCmd::moveto(CStrs& args)
{
    assert(p_arm_!=nullptr);
    auto& arm = *p_arm_;

    if(!checkInit(args))
        return false;

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
    log_i("run cmd moveto:"+st.str());

    //---- run
    arm.moveTo(st);

    return true;
}

//----- arm server
bool ArmCmd::run_server(CStrs& args)
{
    socket::Server svr;

    StrTbl kv; parseKV(args, kv);
    string s_port = lookup(kv, string("port"));
    int port=0; 
    if(!s2d(s_port, port))
    {
        log_e(" failed to get para 'port'");
        return false;
    }
    
    //-----
    bool ok = svr.start(port);
    if(!ok)
    {
        log_e("Failed to start server at port:"+to_string(port));
        return false;
    }
    //---- server started

    while(svr.isRunning())
    {
        string scmd;
        if(!svr.readLn(scmd)) 
            break;

        //---- run cmd
        data_.s_jres = "{}"; // to be filled by runcmd
        bool ok = this->run(scmd);
        string sj = string("{") +
            (ok?"'ack':'ok'" :"'ack':'fail'") +
            "'res':" + data_.s_jres +
            "}\n";
        svr.send(sj);

        sys::sleepMS(200);
    }
    log_i("Server shutdown");
    //---- 
    return true;
}

//----
bool ArmCmd::getSt()
{
    if(p_arm_==nullptr)
        return false;
    ArmSt st;
    bool ok = p_arm_->getSt(st);
    data_.s_jres = enc_json(st);
    return ok;
}

