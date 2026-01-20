class GTConfig:

    def __init__(self, covs, **kwargs):
        self.covs = covs
        self.outdir = kwargs.get("outdir")
        self.minimum_coverage = kwargs.get("minimum_coverage")
        self.t_step = kwargs.get("t_step")
        self.kmax = kwargs.get("k_max")
        self.bootstrap_replicates = kwargs.get("bootstrap_replicates")
        self.verbose = kwargs.get("verbose")
