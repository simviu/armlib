#pragma once

#include "arm/armLib.h"

using namespace arm;

#ifdef WITH_ARM_Z1

#include "control/unitreeArm.h"

namespace unitree{
    //----
    class ArmZ1 : public Arm
    {
    public:
        ArmZ1()
        {
            pCtrlComp_ = new CtrlComponents(0.002);
            p_uarm_ = new unitreeArm(pCtrlComp_);
        }

        virtual bool init()override;
        virtual bool moveTo(const TipSt& ts) override;
        virtual ArmSt getSt()const override; 
        virtual bool test()override;
     //   virtual bool done()const override;
    protected:
        CtrlComponents* pCtrlComp_ = nullptr;
        unitreeArm* p_uarm_ = nullptr;
    };
}

#endif // #ifdef WITH_ARM_Z1
