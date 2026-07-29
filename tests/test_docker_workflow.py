"""Regression checks for the GHCR publishing workflow."""

from pathlib import Path
import unittest


WORKFLOW = (
    Path(__file__).parents[1] / ".github" / "workflows" / "docker-publish.yml"
)


class DockerWorkflowTest(unittest.TestCase):
    def test_uses_supported_actions_and_buildkit_cache(self):
        workflow = WORKFLOW.read_text()

        for action in (
            "actions/checkout@v7",
            "docker/setup-qemu-action@v4",
            "docker/setup-buildx-action@v4",
            "docker/login-action@v4",
            "docker/metadata-action@v6",
            "docker/build-push-action@v7",
        ):
            with self.subTest(action=action):
                self.assertIn(action, workflow)

        self.assertIn("cache-from: type=gha", workflow)
        self.assertIn("cache-to: type=gha,mode=max", workflow)
        self.assertNotIn("actions/cache@", workflow)
        self.assertNotIn("/tmp/.buildx-cache", workflow)


if __name__ == "__main__":
    unittest.main()
