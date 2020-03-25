#ifndef EPIDEMIC_HPP
#define EPIDEMIC_HPP

#include <random>

#include <sst/core/component.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>

#define POPULATION_TOTAL 7760000000

class epidemic : public SST::Component {

public:

    epidemic(SST::ComponentId_t, SST::Params &);

    void setup() override;

    void finish() override;

    bool tick(SST::Cycle_t);

    static void align_signal_width(int, std::string &);

    static void append_signal(char, int, std::string &);

    static std::string align_signal_width(int, float);

    void write_stats_to_mem(std::string &, unsigned int);

    void flash_mem(SST::Event *);

    void mutation(SST::Event *);

    void mul_inv_sev(SST::Event *);

    void mul_inv_inf(SST::Event *);

    void mul_inv_br(SST::Event *);

    void mul_inv_rsrch(SST::Event *);

    void mul_inv_fat(SST::Event *);

    void min_fat(SST::Event *);

    void min_inf(SST::Event *);

    void floor_cure_thresh(SST::Event *);

    void floor_pop_inf(SST::Event *);

    void floor_pop_dead(SST::Event *);

    void mul_pop_inf(SST::Event *);

    void mul_pop_dead(SST::Event *);

    SST_ELI_REGISTER_COMPONENT(
            epidemic,
            "epidemic",
            "epidemic",
            SST_ELI_ELEMENT_VERSION(1, 0, 0),
            "Simulator for the epidemic",
            COMPONENT_CATEGORY_UNCATEGORIZED
    )

    SST_ELI_DOCUMENT_PARAMS(
    )

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS(
            { "mul_inv_sev_din", "mul_inv_sev_din", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_sev_dout", "mul_inv_sev_dout", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_inf_din", "mul_inv_inf_din", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_inf_dout", "mul_inv_inf_dout", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_fat_din", "mul_inv_fat_din", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_fat_dout", "mul_inv_fat_dout", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_br_din", "mul_inv_br_din", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_br_dout", "mul_inv_br_dout", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_rsrch_din", "mul_inv_rsrch_din", { "sst.Interfaces.StringEvent" }},
            { "mul_inv_rsrch_dout", "mul_inv_rsrch_dout", { "sst.Interfaces.StringEvent" }},
            { "mul_pop_inf_din", "mul_pop_inf_din", { "sst.Interfaces.StringEvent" }},
            { "mul_pop_inf_dout", "mul_pop_inf_dout", { "sst.Interfaces.StringEvent" }},
            { "mul_pop_dead_din", "mul_pop_dead_din", { "sst.Interfaces.StringEvent" }},
            { "mul_pop_dead_dout", "mul_pop_dead_dout", { "sst.Interfaces.StringEvent" }},
            { "floor_pop_dead_din", "floor_pop_dead_din", { "sst.Interfaces.StringEvent" }},
            { "floor_pop_dead_dout", "floor_pop_dead_dout", { "sst.Interfaces.StringEvent" }},
            { "min_fat_din", "min_fat_din", { "sst.Interfaces.StringEvent" }},
            { "min_fat_dout", "min_fat_dout", { "sst.Interfaces.StringEvent" }},
            { "min_inf_din", "min_inf_din", { "sst.Interfaces.StringEvent" }},
            { "min_inf_dout", "min_inf_dout", { "sst.Interfaces.StringEvent" }},
            { "floor_cure_thresh_din", "floor_cure_thresh_din", { "sst.Interfaces.StringEvent" }},
            { "floor_cure_thresh_dout", "floor_cure_thresh_dout", { "sst.Interfaces.StringEvent" }},
            { "floor_pop_inf_din", "floor_pop_inf_din", { "sst.Interfaces.StringEvent" }},
            { "floor_pop_inf_dout", "floor_pop_inf_dout", { "sst.Interfaces.StringEvent" }},
            { "flash_mem_din", "flash_mem_din", { "sst.Interfaces.StringEvent" }},
            { "flash_mem_dout", "flash_mem_dout", { "sst.Interfaces.StringEvent" }},
            { "mutation_din", "mutation_din", { "sst.Interfaces.StringEvent" }},
            { "mutation_dout", "mutation_dout", { "sst.Interfaces.StringEvent" }},
    )

private:

    // SST parameters
    uint16_t seed;

    // RNG attributes
    std::mt19937 m_gen;
    std::uniform_int_distribution<unsigned int> m_dis;

    // SST attributes
    SST::Output m_output;
    SST::Link *flash_mem_din_link, *flash_mem_dout_link,
            *mutation_din_link, *mutation_dout_link,
            *mul_inv_sev_din_link, *mul_inv_sev_dout_link,
            *mul_inv_br_din_link, *mul_inv_br_dout_link,
            *mul_inv_inf_din_link, *mul_inv_inf_dout_link,
            *mul_inv_fat_din_link, *mul_inv_fat_dout_link,
            *mul_inv_rsrch_din_link, *mul_inv_rsrch_dout_link,
            *mul_pop_inf_din_link, *mul_pop_inf_dout_link,
            *mul_pop_dead_din_link, *mul_pop_dead_dout_link,
            *floor_cure_thresh_din_link, *floor_cure_thresh_dout_link,
            *floor_pop_inf_din_link, *floor_pop_inf_dout_link,
            *floor_pop_dead_din_link, *floor_pop_dead_dout_link,
            *min_fat_din_link, *min_fat_dout_link,
            *min_inf_din_link, *min_inf_dout_link;

    // main loop attributes
    unsigned int SIMTIME = 2000;
    unsigned int LOOPBEGIN = 2;
    unsigned int LOOPEND = (SIMTIME - 2);
    unsigned int m_cycle{};
    bool m_keep_send{}, m_keep_recv{};
    bool m_mutate_lock = false, m_loop_lock = true, m_mem_read_flag = false, m_cure_found = false, m_eradicated = false;

    // simulation values
    unsigned int m_limit{}, m_cure_threshold{}, m_batch_infected{}, m_total_infected{}, m_total_infected_today{}, m_total_dead_today{}, m_gene{};
    float m_severity{}, m_infectivity{}, m_fatality{}, m_birth_rate{}, m_cure{}, m_research{};
    std::string m_mutation = "0";

    // flash memory variables
    std::string m_mem_read = "101", m_mem_write = "111", m_mem_data_out;
    FILE *m_fp{};

};

#endif
