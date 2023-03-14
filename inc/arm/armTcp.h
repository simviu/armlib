#pragma once

#include "arm/armLib.h"

namespace arm{
    //----
    class ArmTcp : public Arm
    {
    public:

        ArmTcp(const string& sHost, int port);
        ArmTcp(const string& sUri); // 'host:port'

        struct Cfg{
            float fps_st = 10.0;
        }; Cfg cfg_;

        virtual bool init()override;
        virtual bool release()override;
        virtual bool reset()override;
        virtual bool moveTo(const TipSt& ts, float spd) override;
        virtual bool getSt(ArmSt& st) override; 
        virtual bool test()override;

        // init remote arm
        bool init_arm(const string& sModel);
    protected:
        socket::Client client_;
        struct Data{
            ArmSt cur_st;
            bool b_st_val = false;
            //mth::Pipe<string> cmds; // cmd que            
        }; Data data_;
        
        std::mutex mtx_st_; 

        bool run_once(); // one run in thread loop
        bool read_st();
        //bool send_cmds();

        bool send(const string& scmd);
        bool getAck(Cmd::Ack& ack);
        //---
        std::thread thd_;
        std::mutex  thd_mtx_;
    };
}
