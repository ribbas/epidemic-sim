#include "epidemic.hpp"
#include "event_drivers.hpp"
#include "setup.hpp"

bool epidemic::tick(SST::Cycle_t current_cycle) {

    m_keep_send = current_cycle < SIMTIME;
    m_keep_recv = current_cycle < SIMTIME - 1;
    m_cycle = current_cycle;
    std::string current_cycle_str = std::to_string(current_cycle);

    std::string ram_data, ram_addr, rand_int_str;

    if (m_mem_read_flag) {

        ram_addr = std::to_string(current_cycle % (SIMTIME / 2));
        align_signal_width(4, ram_addr);
        flash_mem_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(m_keep_send) +
                std::to_string(m_keep_recv) +
                ram_addr +
                m_mem_read +
                ram_addr
        ));

    } else {

        if (m_total_infected > m_cure_threshold) {

            // random int between 2 and 100
            m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(2, 10));
            rand_int_str = std::to_string(m_dis(m_gen));
            align_signal_width(4, rand_int_str);

            mul_inv_rsrch_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    rand_int_str
            ));

            // random int between 0 and 8
            m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(0, 8));
            m_mutation = std::to_string(m_dis(m_gen));

            mutation_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    std::to_string(m_fatality).back() +
                    m_mutation
            ));

            m_cure += m_research;
        }

        if (current_cycle == 1) {

            m_output.verbose(CALL_INFO, 1, 0, "----------------------------------------\n");
            m_output.verbose(CALL_INFO, 1, 0, "--------- SIMULATION INITIATED ---------\n");
            m_output.verbose(CALL_INFO, 1, 0, "----------------------------------------\n");
            m_output.verbose(CALL_INFO, 1, 0, "   Day  |  Cure  | Infected | Dead\n");
            m_output.verbose(CALL_INFO, 1, 0, "--------+--------+----------+---------\n");

            // random int between 100 and 1023
            m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(100, 1023));
            m_limit = m_dis(m_gen);

            // random int between 100 and m_limit
            m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(100, m_limit));
            rand_int_str = std::to_string(m_dis(m_gen));
            align_signal_width(4, rand_int_str);
            mul_inv_sev_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    rand_int_str
            ));

            // random int between 100 and m_limit
            m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(100, m_limit));
            rand_int_str = std::to_string(m_dis(m_gen));
            align_signal_width(4, rand_int_str);
            mul_inv_br_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    rand_int_str
            ));

        }

        if (current_cycle == LOOPBEGIN + 1) {

            floor_cure_thresh_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    align_signal_width(12, m_severity * m_birth_rate * POPULATION_TOTAL)
            ));

        }

        if (current_cycle > 1 && m_keep_recv) {

            // random int between 100 and m_limit
            m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(100, m_limit));
            rand_int_str = std::to_string(m_dis(m_gen));
            align_signal_width(4, rand_int_str);
            mul_inv_fat_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    rand_int_str
            ));

            // random int between 100 and m_limit
            m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(100, m_limit));
            rand_int_str = std::to_string(m_dis(m_gen));
            align_signal_width(4, rand_int_str);
            mul_inv_inf_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    rand_int_str
            ));

            if (m_cure_found) {

                // random int between 1 and 10
                m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(0, 100));
                m_extra_cycles++;

                if (!m_batch_infected or (m_extra_cycles + current_cycle) > 1021) {
                    m_eradicated = true;
                    m_cure_found = false;
                }

            } else {

                // random int between 1 and 10
                m_dis.param(std::uniform_int_distribution<unsigned int>::param_type(current_cycle, 1998));

            }

            m_batch_infected = m_dis(m_gen);

        }

        if (!m_keep_send) {

            m_output.verbose(CALL_INFO, 1, 0, "Reading Memory...\n");
            m_mem_read_flag = true;
            SIMTIME = current_cycle * 2;
            m_fp = std::fopen((std::to_string(seed) + ".txt").c_str(), "w");

        }

        if (!m_keep_recv) {

            floor_cure_thresh_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0.0000000000"
            ));

            mul_inv_sev_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0000"
            ));

            mul_inv_br_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0000"
            ));

            mul_inv_fat_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0000"
            ));

            mul_inv_inf_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0000"
            ));

            // disable randf_rsrch
            mul_inv_rsrch_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0000"
            ));

        }

        m_total_infected += m_total_infected_today;

        if (m_eradicated && m_loop_lock) {

            int _current_cycle = current_cycle + m_extra_cycles;
            SIMTIME = _current_cycle;
            LOOPEND = (SIMTIME - 2);
            m_loop_lock = false;

            char _factor = std::to_string(m_severity).back();
            std::string factor = _factor == '0' ? "1" : std::to_string((int) _factor - 48);

            ram_data = factor;
            align_signal_width(8, ram_data);
            write_stats_to_mem(ram_data, _current_cycle - 7);

            ram_data = std::to_string(m_severity).substr(2, 8);
            append_signal('0', 7, ram_data);
            ram_data = "0" + ram_data;
            write_stats_to_mem(ram_data, _current_cycle - 6);

            ram_data = std::to_string(m_infectivity).substr(2, 8);
            append_signal('0', 7, ram_data);
            ram_data = "0" + ram_data;
            write_stats_to_mem(ram_data, _current_cycle - 5);

            ram_data = std::to_string(m_fatality).substr(2, 8);
            append_signal('0', 7, ram_data);
            ram_data = "0" + ram_data;
            write_stats_to_mem(ram_data, _current_cycle - 4);

            ram_data = std::to_string(m_birth_rate).substr(2, 8);
            append_signal('0', 7, ram_data);
            ram_data = "0" + ram_data;
            write_stats_to_mem(ram_data, _current_cycle - 3);

            ram_data = std::to_string(m_cure_threshold);
            align_signal_width(8, ram_data);
            write_stats_to_mem(ram_data, _current_cycle - 2);

            m_output.verbose(CALL_INFO, 1, 0, "Factor: %s\n", factor.c_str());
            m_output.verbose(CALL_INFO, 1, 0, "Severity: %f\n", m_severity);
            m_output.verbose(CALL_INFO, 1, 0, "Infectivity: %f\n", m_infectivity);
            m_output.verbose(CALL_INFO, 1, 0, "Fatality: %f\n", m_fatality);
            m_output.verbose(CALL_INFO, 1, 0, "Birth rate: %f\n", m_birth_rate);
            m_output.verbose(CALL_INFO, 1, 0, "Cure threshold: %d\n", m_cure_threshold);

        } else if (!m_eradicated) {

            std::string _cure;
            if (float_less_than(m_cure, 100.00)) {
                _cure = std::to_string((unsigned int) m_cure);
                align_signal_width(2, _cure);
            } else {
                _cure = "00";
                m_cure_found = true;
            }
            m_output.verbose(CALL_INFO, 1, 0, " %6lu | %6.2f | %8d | %8d\n", current_cycle,
                             m_cure, m_total_infected_today, m_total_dead_today);

            std::string _pop_inf = std::to_string(m_total_infected_today);
            std::string _pop_dead = std::to_string(m_total_dead_today);
            align_signal_width(3, _pop_inf);
            align_signal_width(3, _pop_dead);
            ram_data = _pop_dead + _pop_inf + _cure;
            ram_addr = current_cycle_str;
            align_signal_width(4, ram_addr);

            flash_mem_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    ram_addr +
                    m_mem_write +
                    ram_data
            ));

        }

    }  // m_mem_read_flag

    if (current_cycle == SIMTIME) {
        primaryComponentOKToEndSim();
    }

    return current_cycle == SIMTIME;

}
