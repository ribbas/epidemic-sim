#ifndef EPIDEMIC_SETUP_HPP
#define EPIDEMIC_SETUP_HPP

#include <cmath>
#include <limits>

#include "epidemic.hpp"

epidemic::epidemic(SST::ComponentId_t id, SST::Params &params) :
        SST::Component(id),
        // Collect all the parameters from the project driver
        seed(params.find<uint16_t>("SEED", 0)),
        m_gen(seed),
        // initialize ram links
        flash_mem_din_link(configureLink("flash_mem_din")),
        flash_mem_dout_link(configureLink(
                "flash_mem_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::flash_mem))
        ),
        // initialize mutation links
        mutation_din_link(configureLink("mutation_din")),
        mutation_dout_link(configureLink(
                "mutation_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::mutation))
        ),
        // initialize mutation RNG links
        mul_inv_sev_din_link(configureLink("mul_inv_sev_din")),
        mul_inv_sev_dout_link(configureLink(
                "mul_inv_sev_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::mul_inv_sev))
        ),
        // initialize birth rate multiplicative inverse links
        mul_inv_br_din_link(configureLink("mul_inv_br_din")),
        mul_inv_br_dout_link(configureLink(
                "mul_inv_br_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::mul_inv_br))
        ),
        // initialize mutation RNG links
        mul_inv_inf_din_link(configureLink("mul_inv_inf_din")),
        mul_inv_inf_dout_link(configureLink(
                "mul_inv_inf_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::mul_inv_inf))
        ),
        // initialize fatality multiplicative inverse links
        mul_inv_fat_din_link(configureLink("mul_inv_fat_din")),
        mul_inv_fat_dout_link(configureLink(
                "mul_inv_fat_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::mul_inv_fat))
        ),
        // initialize research multiplicative inverse links
        mul_inv_rsrch_din_link(configureLink("mul_inv_rsrch_din")),
        mul_inv_rsrch_dout_link(configureLink(
                "mul_inv_rsrch_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::mul_inv_rsrch))
        ),
        // initialize mul population infected links
        mul_pop_inf_din_link(configureLink("mul_pop_inf_din")),
        mul_pop_inf_dout_link(configureLink(
                "mul_pop_inf_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::mul_pop_inf))
        ),
        // initialize mul batch infected links
        mul_pop_dead_din_link(configureLink("mul_pop_dead_din")),
        mul_pop_dead_dout_link(configureLink(
                "mul_pop_dead_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::mul_pop_dead))
        ),
        // initialize cure threshold floor links
        floor_cure_thresh_din_link(configureLink("floor_cure_thresh_din")),
        floor_cure_thresh_dout_link(configureLink(
                "floor_cure_thresh_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::floor_cure_thresh))
        ),
        // initialize population infected floor links
        floor_pop_inf_din_link(configureLink("floor_pop_inf_din")),
        floor_pop_inf_dout_link(configureLink(
                "floor_pop_inf_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::floor_pop_inf))
        ),
        // initialize population dead floor links
        floor_pop_dead_din_link(configureLink("floor_pop_dead_din")),
        floor_pop_dead_dout_link(configureLink(
                "floor_pop_dead_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::floor_pop_dead))
        ),
        // initialize minimum lethality links
        min_fat_din_link(configureLink("min_fat_din")),
        min_fat_dout_link(configureLink(
                "min_fat_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::min_fat))
        ),
        // initialize minimum infectivity links
        min_inf_din_link(configureLink("min_inf_din")),
        min_inf_dout_link(configureLink(
                "min_inf_dout",
                new SST::Event::Handler<epidemic>(this, &epidemic::min_inf))
        ),
        m_cure_threshold(0), m_batch_infected(0), m_total_infected(0), m_total_infected_today(0),
        m_total_dead_today(0), m_gene(0),
        m_severity(0.0), m_infectivity(0.0), m_fatality(0.0), m_birth_rate(0.0), m_cure(0.0), m_research(0.0) {

    m_output.init("\033[93mepidemic-" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    m_output.setVerboseLevel(0);
    // Just register a plain clock for this simple example
    registerClock("1Hz", new SST::Clock::Handler<epidemic>(this, &epidemic::tick));

    registerAsPrimaryComponent();
    primaryComponentDoNotEndSim();

}

void epidemic::setup() {

    m_output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");

}

void epidemic::finish() {

    m_output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());
    std::fclose(m_fp);

}

void epidemic::align_signal_width(int width, std::string &signal) {
    int _len = signal.length();
    if (_len < width) {
        signal = std::string(width - _len, '0') + signal;
    }
}

void epidemic::append_signal(const char chr, int width, std::string &signal) {
    int _len = signal.length();
    if (_len < width) {
        signal += std::string(width - _len, chr);
    }
}

std::string epidemic::align_signal_width(int width, float signal) {
    std::ostringstream _data_out;
    _data_out << std::fixed << std::setprecision(width) << signal;
    return _data_out.str().substr(0, width);
}

bool float_less_than(float a, float b) {
    return (b - a) >
           ((std::fabs(a) < std::fabs(b) ? std::fabs(b) : std::fabs(a)) * std::numeric_limits<float>::epsilon());
}

void epidemic::write_stats_to_mem(std::string &ram_data, unsigned int cycle) {

    std::string ram_addr = std::to_string(cycle);
    align_signal_width(4, ram_addr);
    flash_mem_din_link->send(new SST::Interfaces::StringEvent(
            std::to_string(m_keep_send) +
            std::to_string(m_keep_recv) +
            ram_addr +
            m_mem_write +
            ram_data
    ));

}

#endif
