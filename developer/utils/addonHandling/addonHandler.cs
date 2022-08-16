using System;

namespace developerCS.utils.addonHandling
{
    public class AddonHandling
    {
        readonly Utils utils;

        public AddonHandling(Utils utils)
        {
            this.utils = utils;
            invokeAddonHandler();
        }

        private void invokeAddonHandler()
        {
            ImportAddon importAddon = new(utils);
        }
    }
}