#include <random>

#include <systemc.h>

SC_MODULE(rng) {
    sc_in_clk clock;
    sc_in<bool> en;
    sc_in<sc_uint<16> > seed;
    sc_in<sc_uint<8> > lower_limit;
    sc_in<sc_uint<10> > upper_limit;
    sc_out<sc_uint<10> > data_out;

    std::mt19937 generator;  // standard mersenne_twister_engine

    /* initialize random seed: */
    void new_seed() {
        generator.seed((unsigned int) seed.read());
    }

    void generate() {

        std::uniform_int_distribution<unsigned int> distr(lower_limit.read(), upper_limit.read());

        if ((lower_limit.read() < upper_limit.read()) && en.read()) {
            data_out.write(distr(generator));
        }
    }

    SC_CTOR(rng) {
        SC_METHOD(new_seed);
        SC_METHOD(generate);
        sensitive << clock;
    }
};
