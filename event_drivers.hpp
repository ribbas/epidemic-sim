#ifndef EPIDEMIC_EVENT_DRIVERS_HPP
#define EPIDEMIC_EVENT_DRIVERS_HPP

#include "epidemic.hpp"
#include "setup.hpp"

void epidemic::flash_mem(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_mem_read_flag) {

        m_mem_data_out = se->getString();
        align_signal_width(8, m_mem_data_out);

        std::string ram_addr = std::to_string(m_cycle % (SIMTIME / 2));
        align_signal_width(6, ram_addr);
        fprintf(m_fp, "%s %s\n", ram_addr.c_str(), m_mem_data_out.c_str());

    }

    delete se;

}

void epidemic::mutation(SST::Event *ev) {

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

void epidemic::mul_inv_inf(SST::Event *ev) {

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
                    align_signal_width(12, m_infectivity + std::stof(se->getString())) +
                    "0.25"
            ));

        }

    }

    delete se;

}

void epidemic::mul_inv_sev(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {

        m_severity = std::stof(se->getString());

    }

    delete se;

}

void epidemic::mul_inv_br(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {
        m_birth_rate = std::stof(se->getString());
    }

    delete se;

}

void epidemic::mul_inv_rsrch(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_keep_recv) {

        m_research = std::stof(se->getString());

    }

    delete se;

}

void epidemic::floor_cure_thresh(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);

    if (se && m_keep_recv) {
        m_cure_threshold = std::stoi(se->getString()) / m_limit;
    }

    delete se;

}

void epidemic::mul_inv_fat(SST::Event *ev) {

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
                    align_signal_width(12, m_fatality + std::stof(se->getString())) +
                    "0.25"
            ));

        }

    }

    delete se;

}

void epidemic::min_fat(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    if (se && m_cycle < LOOPEND) {

        m_fatality = std::stof(se->getString());

    }

    delete se;

}

void epidemic::min_inf(SST::Event *ev) {

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
        align_signal_width(4, batch_inf_str);

        mul_pop_inf_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(_keep_send) +
                std::to_string(_keep_recv) +
                batch_inf_str +
                align_signal_width(12, m_infectivity)
        ));

    }

    delete se;

}

void epidemic::mul_pop_inf(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 3;
    bool _keep_recv = m_cycle < SIMTIME - 4;

    if (se && m_cycle < LOOPEND - 1) {

        floor_pop_inf_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(_keep_send) +
                std::to_string(_keep_recv) +
                align_signal_width(12, std::stof(se->getString()))
        ));

    }

    delete se;

}

void epidemic::floor_pop_inf(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 4;
    bool _keep_recv = m_cycle < SIMTIME - 5;

    if (se && m_cycle < LOOPEND - 2) {

        m_total_infected_today = std::stoi(se->getString());
        std::string m_total_infected_today_str = se->getString();
        align_signal_width(4, m_total_infected_today_str);

        mul_pop_dead_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(_keep_send) +
                std::to_string(_keep_recv) +
                m_total_infected_today_str +
                align_signal_width(12, m_fatality)
        ));

    }

    delete se;

}

void epidemic::mul_pop_dead(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);
    bool _keep_send = m_cycle < SIMTIME - 4;
    bool _keep_recv = m_cycle < SIMTIME - 5;

    if (se && m_cycle < LOOPEND - 1) {

        floor_pop_dead_din_link->send(new SST::Interfaces::StringEvent(
                std::to_string(_keep_send) +
                std::to_string(_keep_recv) +
                align_signal_width(12, std::stof(se->getString()))
        ));

    }

    delete se;

}

void epidemic::floor_pop_dead(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);

    if (se && m_cycle < LOOPEND - 3) {
        m_total_dead_today = std::stoi(se->getString());
    }

    delete se;

}

#endif
