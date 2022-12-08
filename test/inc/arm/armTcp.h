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
        virtual bool moveTo(const TipSt& ts) override;
        virtual ArmSt getSt()const override; 
        virtual bool test()override;
     //   virtual bool done()const override;
    protected:
        socket::Client client_;
        void onRecv(const char* buf, int len);
        
       
    };
}
