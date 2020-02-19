#include "plague.hpp"
#include "setup.hpp"
#include "event_drivers.hpp"

bool plague::tick(SST::Cycle_t current_cycle) {

    m_keep_send = current_cycle < SIMTIME;
    m_keep_recv = current_cycle < SIMTIME - 1;
    m_cycle = current_cycle;
    std::string current_cycle_str = std::to_string(current_cycle);

    std::string ram_data, ram_addr;

    if (m_mem_read_flag) {

        ram_addr = std::to_string(current_cycle % (SIMTIME / 2));
        align_signal_width('0', 6, ram_addr);
        flash_mem_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(m_keep_send) +
                std::to_string(m_keep_recv) +
                ram_addr +
                m_mem_read +
                ram_addr
        ));

    } else {

        if (m_total_infected > m_cure_threshold) {

            randf_rsrch_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "1" +
                    seed_research +
                    "0020100" +
                    current_cycle_str
            ));

            rng_mut_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "1" +
                    seed_mutation +
                    "0000008" +
                    current_cycle_str
            ));

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
            rng_limit_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "1" +
                    seed_lim +
                    "1001023" +
                    current_cycle_str
            ));

        }

        if (current_cycle == LOOPBEGIN + 1) {

            floor_cure_thresh_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    align_signal_width(5, m_severity * m_birth_rate * POPULATION_TOTAL)
            ));

        }

        if (current_cycle > 1 && m_keep_recv) {

            randf_fat_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "1" +
                    seed_let +
                    "002" +
                    m_limit +
                    current_cycle_str
            ));

            randf_inf_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "1" +
                    seed_inf +
                    "002" +
                    m_limit +
                    current_cycle_str
            ));

            rng_pop_inf_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "1" +
                    seed_pop_inf +
                    "0010010" +
                    current_cycle_str
            ));

        }

        if (!m_keep_send) {

            std::cout << current_cycle << " Reading Memory...\n";
            m_mem_read_flag = true;
            SIMTIME = current_cycle * 2;
            m_fp = std::fopen("memory_dump.txt", "w");

        }

        if (!m_keep_recv) {

            rng_limit_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0" +
                    seed_lim +
                    "0201000" +
                    current_cycle_str
            ));

            randf_sev_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0" +
                    seed_sev +
                    "002" +
                    current_cycle_str
            ));

            randf_br_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0" +
                    seed_birth_rate +
                    "002" +
                    current_cycle_str
            ));

            floor_cure_thresh_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0.0000000000"
            ));

            randf_fat_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0" +
                    seed_let +
                    "002" +
                    m_limit +
                    current_cycle_str
            ));

            randf_inf_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0" +
                    seed_inf +
                    "002" +
                    m_limit +
                    current_cycle_str
            ));

            randf_rsrch_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0" +
                    seed_research +
                    "0020100" +
                    current_cycle_str
            ));

            rng_mut_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0" +
                    seed_mutation +
                    "0020008" +
                    current_cycle_str
            ));

            rng_pop_inf_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    "0" +
                    seed_pop_inf +
                    "0020010" +
                    current_cycle_str
            ));

        }

        m_total_infected += m_total_infected_today;
        m_total_dead += m_total_dead_today;

        if (less_than(100.00, m_cure) && m_loop_lock) {

            std::cout << "ENDING " << m_cure << '\n';
            SIMTIME = current_cycle + 6;
            LOOPEND = (SIMTIME - 2);
            m_loop_lock = false;

            ram_data = std::to_string(m_severity).substr(2, 8);
            append_signal('0', 7, ram_data);
            ram_data = "0" + ram_data;
            ram_addr = std::to_string(current_cycle);
            align_signal_width('0', 6, ram_addr);
            flash_mem_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    ram_addr +
                    m_mem_write +
                    ram_data
            ));

            ram_data = std::to_string(m_infectivity).substr(2, 8);
            append_signal('0', 7, ram_data);
            ram_data = "0" + ram_data;
            ram_addr = std::to_string(current_cycle + 1);
            align_signal_width('0', 6, ram_addr);
            flash_mem_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    ram_addr +
                    m_mem_write +
                    ram_data
            ));

            ram_data = std::to_string(m_fatality).substr(2, 8);
            append_signal('0', 7, ram_data);
            ram_data = "0" + ram_data;
            ram_addr = std::to_string(current_cycle + 2);
            align_signal_width('0', 6, ram_addr);
            flash_mem_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    ram_addr +
                    m_mem_write +
                    ram_data
            ));

            ram_data = std::to_string(m_birth_rate).substr(2, 8);
            append_signal('0', 7, ram_data);
            ram_data = "0" + ram_data;
            ram_addr = std::to_string(current_cycle + 3);
            align_signal_width('0', 6, ram_addr);
            flash_mem_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    ram_addr +
                    m_mem_write +
                    ram_data
            ));

            ram_data = std::to_string(m_cure_threshold);
            align_signal_width('0', 8, ram_data);
            ram_addr = std::to_string(current_cycle + 4);
            align_signal_width('0', 6, ram_addr);
            flash_mem_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(m_keep_send) +
                    std::to_string(m_keep_recv) +
                    ram_addr +
                    m_mem_write +
                    ram_data
            ));

            m_output.verbose(CALL_INFO, 1, 0, "Severity: %f\n", m_severity);
            m_output.verbose(CALL_INFO, 1, 0, "Infectivity: %f\n", m_infectivity);
            m_output.verbose(CALL_INFO, 1, 0, "Fatality: %f\n", m_fatality);
            m_output.verbose(CALL_INFO, 1, 0, "Birth rate: %f\n", m_birth_rate);
            m_output.verbose(CALL_INFO, 1, 0, "Cure threshold: %d\n", m_cure_threshold);

        } else if (less_than(m_cure, 100.00)) {

            // std::cout << "NOPE " << m_cure << '\n';
            m_output.verbose(CALL_INFO, 1, 0, " %6lu | %6.2f | %8d | %8d\n", current_cycle,
                             m_cure, m_total_infected_today, m_total_dead_today);

            std::string _pop_inf = std::to_string(m_total_infected_today);
            std::string _pop_dead = std::to_string(m_total_dead_today);
            std::string _cure = std::to_string((unsigned int) m_cure);
            align_signal_width('0', 3, _pop_inf);
            align_signal_width('0', 3, _pop_dead);
            align_signal_width('0', 2, _cure);
            ram_data = _pop_inf + _pop_dead + _cure;
            ram_addr = current_cycle_str;
            align_signal_width('0', 6, ram_addr);

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
