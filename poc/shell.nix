with import <nixpkgs> {};
let

  python =
    python3.withPackages(ps:
      with ps; [ rply appdirs ]
    );
    
in stdenv.mkDerivation rec {
  name = "rt-learn";

  buildInputs = [ python ];

  env = buildEnv { name = name; paths = buildInputs; };
}
