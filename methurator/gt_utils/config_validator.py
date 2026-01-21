class GTConfig:

    def __init__(self, covs, **kwargs):
        self.covs = covs
        self.outdir = kwargs.get("outdir")
        self.minimum_coverage = kwargs.get("minimum_coverage")
        self.t_step = kwargs.get("t_step")
        self.t_max = kwargs.get("t_max")
        self.mu = kwargs.get("mu")
        self.size = kwargs.get("size")
        self.mt = kwargs.get("mt")
        self.compute_ci = kwargs.get("compute_ci")
        self.bootstrap_replicates = kwargs.get("bootstrap_replicates")
        self.conf = kwargs.get("conf")
        self.verbose = kwargs.get("verbose")
