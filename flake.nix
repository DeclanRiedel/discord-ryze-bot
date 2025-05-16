{
  description = "Discord Reaction Role Bot Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonEnv =
          pkgs.python3.withPackages (ps: with ps; [ discordpy python-dotenv ]);
      in { devShell = pkgs.mkShell { buildInputs = [ pythonEnv ]; }; });
}
