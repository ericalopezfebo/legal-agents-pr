from legal_agents_pr.cli.main import main


def test_cli_list(capsys):
    assert main(["list"]) == 0
    assert "administrative-law" in capsys.readouterr().out


def test_cli_route(capsys):
    assert main(["route", "revisión judicial de agencia"]) == 0
    assert "administrative-law" in capsys.readouterr().out


def test_cli_sources(capsys):
    assert main(["sources"]) == 0
    output = capsys.readouterr().out
    assert "pr-lpau-38-2017-2025-05-16" in output
    assert "pr-professional-conduct-rules-er-2025-02" in output


def test_cli_source(capsys):
    assert main(["source", "pr-civil-code-55-2020-2024-08-20"]) == 0
    assert "Código Civil de 2020" in capsys.readouterr().out


def test_cli_unknown_source_fails_safely(capsys):
    assert main(["source", "missing-source"]) == 2
    assert "Unknown source: missing-source" in capsys.readouterr().err


def test_cli_authority_candidates_are_explicitly_unverified(capsys):
    assert main(["authorities", "--topic", "obligaciones", "--limit", "3"]) == 0
    output = capsys.readouterr().out
    assert output.count("UNVERIFIED") == 3
    assert "Obligaciones" in output
