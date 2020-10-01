with import <nixpkgs> {};
mkShell {
  buildInputs = [
    (with pkgs.python36Packages; [ matplotlib numpy ])
  ];
}
