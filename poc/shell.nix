with import <nixpkgs> {};
let

  python =
    python3.withPackages(ps:
      with ps; [ rply appdirs ]
    );
    
in stdenv.mkDerivation rec {
  name = "fx-lang";

  buildInputs = [ python ];

  env = buildEnv { name = name; paths = buildInputs; };
}
