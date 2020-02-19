#ifndef PLAGUE_EVENT_DRIVERS_HPP
#define PLAGUE_EVENT_DRIVERS_HPP

#include "plague.hpp"
#include "setup.hpp"

#include <iomanip>

void plague::flash_mem(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_mem_read_flag) {

        m_mem_data_out = se->getString();
        align_signal_width('0', 8, m_mem_data_out);

        std::string ram_addr = std::to_string(m_cycle % (SIMTIME / 2));
        align_signal_width('0', 6, ram_addr);
        fprintf(m_fp, "%s %s\n", ram_addr.c_str(), m_mem_data_out.c_str());

    }

    delete se;

}

void plague::mutation(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {

        m_gene = std::stoi(se->getString());
        switch (m_gene) {
            case 0:
                // no mutation
                break;
            case 1:
                // mutation that decreases infectivity of strain
                m_infectivity = abs(m_infectivity - m_research);
                m_mutate_lock = true;
                break;
            case 2:
                // mutation that increases immunity of strain
                m_cure -= m_research;
                break;
        }

    }

    delete se;

}

void plague::rng_limit(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {

        m_limit = se->getString();
        align_signal_width('0', 4, m_limit);
        std::cout << m_cycle << " LIM " << m_limit << '\n';

        randf_sev_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(m_keep_send) +
                std::to_string(m_keep_recv) +
                "1" +
                seed_sev +
                "020" +
                m_limit +
                std::to_string(m_cycle)
        ));

        randf_br_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(m_keep_send) +
                std::to_string(m_keep_recv) +
                "1" +
                seed_birth_rate +
                "020" +
                m_limit +
                std::to_string(m_cycle)
        ));

    }

    delete se;

}

void plague::rng_mut(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {

        m_mutation = se->getString();

    }

    delete se;

}

void plague::randf_rsrch(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {

        m_research = std::stof(se->getString());

    }

    delete se;

}

void plague::randf_sev(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {

        m_severity = std::stof(se->getString());
        std::cout << m_cycle << " m_severity " << m_severity << '\n';
    }

    delete se;

}

void plague::randf_br(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {

        m_birth_rate = std::stof(se->getString());
        std::cout << m_cycle << " m_birth_rate " << m_birth_rate << '\n';
    }

    delete se;

}

void plague::floor_cure_thresh(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);

    if (se && m_keep_recv) {

        m_cure_threshold = std::stoi(se->getString()) / std::stoi(m_limit);
        std::cout << m_cycle << " m_severity " << m_severity << '\n';
        std::cout << m_cycle << " m_birth_rate " << m_birth_rate << '\n';
        std::cout << m_cycle << " pop " << POPULATION_TOTAL << '\n';
        std::cout << m_cycle << " shouild be " << m_severity * m_birth_rate * POPULATION_TOTAL << '\n';
        std::cout << m_cycle << " CURE THRESH " << std::stoi(se->getString()) << ' ' << std::stoi(m_limit) <<
        ' ' << std::stoi(se->getString()) / std::stoi(m_limit) << '\n';

    }

    delete se;

}

void plague::randf_fat(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 1;
    bool _keep_recv = m_cycle < SIMTIME - 2;

    if (se && m_keep_recv) {

        if (m_cycle == LOOPBEGIN) {

            m_fatality = std::stof(se->getString());

        } else {

            min_fat_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(_keep_send) +
                    std::to_string(_keep_recv) +
                    align_signal_width(10, m_fatality + std::stof(se->getString())) +
                    "0.25"
            ));

        }

    }

    delete se;

}

void plague::min_fat(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_cycle < LOOPEND) {

        m_fatality = std::stof(se->getString());

    }

    delete se;

}

void plague::randf_inf(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 1;
    bool _keep_recv = m_cycle < SIMTIME - 2;

    if (se && m_keep_recv) {

        if (m_cycle == LOOPBEGIN) {

            m_infectivity = std::stof(se->getString());

        } else {

            min_inf_din_link->send(new SST::Interfaces::StringEvent(
                    std::to_string(_keep_send) +
                    std::to_string(_keep_recv) +
                    align_signal_width(10, m_infectivity + std::stof(se->getString())) +
                    "0.25"
            ));

        }

    }

    delete se;

}

void plague::min_inf(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 2;
    bool _keep_recv = m_cycle < SIMTIME - 3;

    if (se && m_cycle < LOOPEND) {

        if (!m_mutate_lock) {
            m_infectivity = std::stof(se->getString());
        } else {
            m_mutate_lock = false;
        }

        std::string batch_inf_str = std::to_string(m_batch_infected);
        align_signal_width('0', 4, batch_inf_str);

        mul_pop_inf_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(_keep_send) +
                std::to_string(_keep_recv) +
                batch_inf_str +
                align_signal_width(10, m_infectivity)
        ));

    }

    delete se;

}

void plague::mul_pop_inf(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 3;
    bool _keep_recv = m_cycle < SIMTIME - 4;

    if (se && m_cycle < LOOPEND - 1) {

        floor_pop_inf_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(_keep_send) +
                std::to_string(_keep_recv) +
                align_signal_width(2, std::stof(se->getString()))
        ));

    }

    delete se;

}

void plague::rng_pop_inf(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);

    if (se && m_cycle < LOOPEND) {

        m_batch_infected = std::stoi(se->getString()) * m_cycle / std::stoi(m_limit) + 1;

    }

    delete se;

}

void plague::floor_pop_inf(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 4;
    bool _keep_recv = m_cycle < SIMTIME - 5;

    if (se && m_cycle < LOOPEND - 2) {

        m_total_infected_today = std::stoi(se->getString());
        std::string m_total_infected_today_str = se->getString();
        align_signal_width('0', 4, m_total_infected_today_str);

        mul_pop_dead_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(_keep_send) +
                std::to_string(_keep_recv) +
                m_total_infected_today_str +
                align_signal_width(10, m_fatality)
        ));

    }

    delete se;

}

void plague::mul_pop_dead(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 4;
    bool _keep_recv = m_cycle < SIMTIME - 5;

    if (se && m_cycle < LOOPEND - 1) {

        floor_pop_dead_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(_keep_send) +
                std::to_string(_keep_recv) +
                align_signal_width(2, std::stof(se->getString()))
        ));

    }

    delete se;

}

void plague::floor_pop_dead(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);

    if (se && m_cycle < LOOPEND - 3) {
        m_total_dead_today = std::stoi(se->getString());
    }

    delete se;

}

#endif
