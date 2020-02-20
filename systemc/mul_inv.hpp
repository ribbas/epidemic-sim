#include <systemc.h>

SC_MODULE(mul_inv) {
    sc_in_clk clock;
    sc_in<sc_uint<10> > operand;
    sc_out<float> data_out;

    void div() {
        data_out.write(1 / ((float) operand.read()));
    }

    SC_CTOR(mul_inv) {
        SC_METHOD(div);
        sensitive << clock;
    }
};
