"""Awx job template helper module."""
import json

from tower_cli.exceptions import Found, NotFound

from .credential import AwxCredential
from .inventory import AwxInventory
from .project import AwxProject
from ..base import AwxBase

# TODO: Add in additional parameters that are optional for all methods.


class AwxJobTemplate(AwxBase):
    """Awx job template class."""
    __resource_name__ = 'job_template'

    def __init__(self):
        """Constructor."""
        super(AwxJobTemplate, self).__init__()
        self._inventory = AwxInventory()
        self._credential = AwxCredential()
        self._project = AwxProject()

    @property
    def project(self):
        """Return project instance."""
        return self._project

    @property
    def credential(self):
        """Return credential instance."""
        return self._credential

    @property
    def inventory(self):
        """Return inventory instance."""
        return self._inventory

    @property
    def job_templates(self):
        """Return a list of job templates."""
        return self.resource.list()

    def create(self, name, description, job_type, inventory, project, playbook,
               credential, extra_vars=None):
        """Create a job template.

        :param name: Template name.
        :type name: str
        :param description: Template description.
        :type description: str
        :param job_type: Job type.
        :type job_type: str
        :param inventory: Inventory name.
        :type inventory: str
        :param project: Project name.
        :type project: str
        :param playbook: Playbook name.
        :type playbook: str
        :param credential: Credential name.
        :type credential: str
        :param extra_vars: Extra variables.
        :type extra_vars: list
        """
        # get credential object
        _credential = self.credential.get(credential)

        # get inventory object
        _inventory = self.inventory.get(inventory)

        # get project object
        _project = self.project.get(project)

        # set extra vars
        _extra_vars = list()
        if extra_vars:
            for elem in extra_vars:
                _extra_vars.append(json.dumps(elem))
        else:
            _extra_vars = None

        try:
            self.resource.create(
                name=name,
                description=description,
                job_type=job_type,
                inventory=_inventory['id'],
                project=_project['id'],
                playbook=playbook,
                credential=_credential['id'],
                extra_vars=_extra_vars
            )
        except Found as ex:
            raise Exception(ex.message)

    def delete(self, name, project):
        """Delete a job template.

        :param name: Template name.
        :type name: str
        :param project: Project name.
        :type project: str
        """
        # get project object
        _project = self.project.get(project)

        # delete job template
        self.resource.delete(name=name, project=_project['id'])

    def get(self, name):
        """Get job template.

        :param name: Template name.
        :type name: str
        :return: Template object.
        :rtype: dict
        """
        try:
            return self.resource.get(name=name)
        except NotFound as ex:
            raise Exception(ex.message)
