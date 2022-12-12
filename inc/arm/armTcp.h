#pragma once

#include "arm/armLib.h"

namespace arm{
    //----
    class ArmTcp : public Arm
    {
    public:
        ArmTcp(const string& sHost, int port);
        ArmTcp(const string& sUri); // 'host:port'

        virtual bool init()override;
        virtual bool release()override;
        virtual bool reset()override;
        virtual bool moveTo(const TipSt& ts, float spd) override;
        virtual ArmSt getSt()const override; 
        virtual bool test()override;
     //   virtual bool done()const override;
    protected:
        socket::Client client_;
        void onRecv(const char* buf, int len);
        struct Data{
            ArmSt cur_st;
        }; Data data_;
        //std::mutex mtx_; TODO:

        //---

       
    };
}
