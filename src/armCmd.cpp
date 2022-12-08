#include "arm/armLib.h"


using namespace arm;

namespace{
    struct LCfg{
    }; LCfg lc_;
}


//-------
ArmCmd::ArmCmd()
{
    

    //----
    {
        add("init", mkSp<Cmd>("init name=[NAME]",
        [&](CStrs& args)->bool{ 
            StrTbl kv; parseKV(args, kv);
            string sN = lookup(kv, "arm");
            p_arm_ = Arm::create(sN);
            if(p_arm_==nullptr)
                return false;
            return p_arm_->init();

        }));
    }
    //----
    {
        add("moveto", mkSp<Cmd>("moveto <x,y,z,rx,ry,rz>",
        [&](CStrs& args)->bool{ return moveto(args); }));
    }
    //----
    {
        add("server", mkSp<Cmd>("server port=PORT",
        [&](CStrs& args)->bool{ return run_server(args); }));
    }
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
    svr.setRcv([&](const char* buf , int len){
        string scmd(buf, len);
        log_i("Run cmd:'"+scmd+"'");

        //---- run cmd
        bool ok = this->run(scmd);
        string sj = string("{") +
            (ok?"'st':'ok'" :"'st':'fail'") +
            "'res':" + data_.s_jres +
            "}";
        svr.send(sj);

    });
    //-----
    bool ok = svr.start(port);
    if(!ok)
    {
        log_e("Failed to start server at port:"+to_string(port));
        return false;
    }
    //---- server started

    while(svr.isRunning())
        sys::sleepMS(200);
    log_i("Server shutdown");
    //---- 
    return true;
}
