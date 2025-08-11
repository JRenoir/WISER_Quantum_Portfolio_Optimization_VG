from pathlib import Path
ROOT = Path(__file__).parent.parent

doe_twolocalxx_common = {
    'lp_file': f'{ROOT}/data/1/31bonds/docplex-bin-avgonly.lp',
    'num_exec': 10,
    'ansatz': 'TwoLocalxx',
    'theta_initial': 'piby3',
    'optimizer': 'nft',
    'device':'AerSimulator',
    'max_epoch': 4,
    'shots': 2**13,
    'theta_threshold': 0.,
    }

doe_twolocal_common = {
    'lp_file': f'{ROOT}/data/1/31bonds/docplex-bin-avgonly.lp',
    'num_exec': 10,
    'ansatz': 'TwoLocal',
    'theta_initial': 'piby3',
    'optimizer': 'nft',
    'device':'AerSimulator',
    'max_epoch': 4,
    'shots': 2**13,
    'theta_threshold': 0.,
    }

doe_bfcd_common = {
    'lp_file': f'{ROOT}/data/1/31bonds/docplex-bin-avgonly.lp',
    'num_exec': 10,
    'ansatz': 'bfcd',
    'theta_initial': 'piby3',
    'optimizer': 'nft',
    'device':'AerSimulator',
    'max_epoch': 4,
    'shots': 2**13,
    'theta_threshold': 0.,
    }

doe_bfcdR_common = {
    'lp_file': f'{ROOT}/data/1/31bonds/docplex-bin-avgonly.lp',
    'num_exec': 10,
    'ansatz': 'bfcdR',
    'theta_initial': 'piby3',
    'optimizer': 'nft',
    'device':'AerSimulator',
    'max_epoch': 4,
    'shots': 2**13,
    'theta_threshold': 0.,
    }


doe = {
    # Twolocalxx bilinear entanglement our core results
    '1/31bonds/TwoLocalxx1rep_piby3_AerSimulator_0.1':
        doe_twolocalxx_common | {
            'experiment_id': 'TwoLocalxx1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    # Twolocalxx smallworld entanglement
    '1/31bonds/TwoLocalxxsw1rep_piby3_AerSimulator_0.1':
        doe_twolocalxx_common | {
            'experiment_id': 'TwoLocalxxsw1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'smallworld'},
            'alpha': 0.1,
            },    
    # Twolocal bilinear entanglement
    '1/31bonds/TwoLocal1rep_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    # Twolocal smallworld entanglement
    '1/31bonds/TwoLocalsw1rep_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocalsw1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'smallworld'},
            'alpha': 0.1,
            },
    # TwoLocal full entanglement
    '1/31bonds/TwoLocal1repFull_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal1repFull_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'full'},
            'alpha': 0.1,
            },
    # BFCD bilinear entanglement
    '1/31bonds/bfcd1rep_piby3_AerSimulator_0.1':
        doe_bfcd_common | {
            'experiment_id': 'bfcd1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    # BFCDR bilinear entanglement
    '1/31bonds/bfcdR1rep_piby3_AerSimulator_0.1':
        doe_bfcdR_common | {
            'experiment_id': 'bfcdR1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    # BFCDR smallworld entanglement
    '1/31bonds/bfcdRsw1rep_piby3_AerSimulator_0.1':
        doe_bfcdR_common | {
            'experiment_id': 'bfcdRsw1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'smallworld'},
            'alpha': 0.1,
            },
    }
