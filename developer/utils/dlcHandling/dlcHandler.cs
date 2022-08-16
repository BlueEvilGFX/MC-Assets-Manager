using System;

namespace developerCS.utils.dlcHandling
{
    public class DLCHandling
    {
        readonly Utils utils;

        public DLCHandling(Utils utils)
        {
            this.utils = utils;
            invokeAddonHandler();
        }

        private void invokeAddonHandler()
        {
            ImportAddon importDLCs = new(utils);
        }
    }
}