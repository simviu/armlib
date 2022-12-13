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
     //   virtual bool done()const override;
    protected:
        socket::Client client_;
        struct Data{
            ArmSt cur_st;
        }; Data data_;
        std::mutex mtx_; 
        void read_st();
        std::thread st_thd_;
    };
}
